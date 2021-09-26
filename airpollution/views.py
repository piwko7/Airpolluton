import colorsys
import json

from django.db.models import Sum, Q, Max, Min
from django.http import HttpResponse
from django.shortcuts import render
from django import forms
import openpyxl

from .models import Pollutant, Country, PollutantEntry
from .helpers import get_headers_and_units, XLEHEADERS

# Create your views here.

# from .models import


class ExcelUploadForm(forms.Form):
    year = forms.CharField(max_length=4)
    file = forms.FileField()


def airpollution(request):
    if request.method == 'GET':
        table_data = {}
        visuals_data = {}
        pollutant_list = [pollutant for pollutant in Pollutant.objects.all()]
        country_list = [country.iso_code for country in Country.objects.all()]

        # populate data from DB
        for pollutant in pollutant_list:
            table_data[pollutant.name] = {}
            visuals_data[pollutant.name] = {'labels': [], 'data': []}
            for country in country_list:
                total = PollutantEntry.objects\
                    .aggregate(total=Sum('pollution_level', filter=Q(pollutant=pollutant,
                                                                     country__iso_code=country)))['total']
                minimum = PollutantEntry.objects \
                    .aggregate(min=Min('pollution_level', filter=Q(pollutant=pollutant,
                                                                     country__iso_code=country)))['min']

                maximum = PollutantEntry.objects \
                    .aggregate(max=Max('pollution_level', filter=Q(pollutant=pollutant,
                                                                     country__iso_code=country)))['max']

                count = PollutantEntry.objects.filter(pollutant=pollutant, country__iso_code=country).count()
                units = PollutantEntry.objects.filter(pollutant=pollutant, country__iso_code=country).first()
                units = units.units if units else ''
                if total is not None and count:
                    table_data[pollutant.name][country] = {'avg': total / count, 'min': minimum, 'max': maximum,
                                                           'limit': pollutant.limit_value, 'units': units}
                    visuals_data[pollutant.name]['labels'].append(country)
                    visuals_data[pollutant.name]['data'].append(total / count)

        # Post process for visual data
        for pollutant_data in visuals_data.values():
            data_count = len(pollutant_data['labels'])
            HSV_tuples = [(i * 1.0 / data_count, 0.5, 0.5) for i in range(data_count)]
            RGB_tuples = map(lambda x: colorsys.hsv_to_rgb(*x), HSV_tuples)
            background_colors = []
            border_colors = []
            for rgb in RGB_tuples:
                red, green, blue = int(rgb[0]*255), int(rgb[1]*255), int(rgb[2]*255)
                background_colors.append(f'rgba({red}, {green}, {blue}, 0.2)')
                border_colors.append(f'rgba({red}, {green}, {blue}, 1)')

            pollutant_data['labels'] = json.dumps(pollutant_data['labels'])
            pollutant_data['data'] = json.dumps(pollutant_data['data'])
            pollutant_data['background'] = json.dumps(background_colors)
            pollutant_data['border'] = json.dumps(border_colors)

        context = {
            'app_name': request.resolver_match.app_name,
            'data': table_data,
            'visuals_data': visuals_data
        }

    elif request.method == 'POST':
        form = ExcelUploadForm(request.POST, request.FILES)
        if form.is_valid():
            year = form.cleaned_data['year']
            file = form.cleaned_data['file']
            work_book = openpyxl.load_workbook(filename=file, read_only=False)
            tabs_name = work_book.get_sheet_names()
            for tab_name in tabs_name:
                work_sheet = work_book[tab_name]
                pollutant_name = tab_name.split('_')[0].strip()
                pollutant = Pollutant.objects.get_or_create(name=pollutant_name)
                if pollutant[0].limit_value is None:
                    limit_value = int(work_sheet['A'][2].value.split()[-2])
                    pollutant[0].limit_value = limit_value
                    pollutant[0].save()
                headers_row, headers, units = get_headers_and_units(work_sheet)


                # save all entries to database
                to_insert = []
                for i, row in enumerate(work_sheet.rows):
                    if i <= headers_row:  # skip to actual entries
                        continue
                    country = row[headers[XLEHEADERS.COUNTRY]].value
                    if country is None:
                        break

                    if len(country) > 2:
                        country_object = Country.objects.filter(name=country).first()
                    else:
                        country_object = Country.objects.get(iso_code=country)

                    city = row[headers[XLEHEADERS.CITY]].value
                    station_name = row[headers[XLEHEADERS.STATION_NAME]].value
                    station_area = row[headers[XLEHEADERS.AREA]].value


                    data = {
                        'pollutant': pollutant[0],
                        'country': country_object,
                        'year': year,
                        'city': city if city else '',
                        'station_code': row[headers[XLEHEADERS.STATION_EOI_CODE]].value,
                        'station_name': station_name if station_name else '',
                        'pollution_level': row[headers[XLEHEADERS.AIR_POLLUTION_LEVEL]].value,
                        'units': units,
                        'station_type': row[headers[XLEHEADERS.TYPE]].value,
                        'station_area': station_area if station_area else '',
                        'longitude': row[headers[XLEHEADERS.LONGITUDE]].value,
                        'latitude': row[headers[XLEHEADERS.LATITUDE]].value,
                        'altitude': row[headers[XLEHEADERS.ALTITUDE]].value,
                    }

                    if country_object is not None:
                        to_insert.append(PollutantEntry(**data))

                PollutantEntry.objects.filter(year=year, pollutant=pollutant[0]).delete()
                PollutantEntry.objects.bulk_create(to_insert)

        context = {
            'app_name': request.resolver_match.app_name,
            'message_success': 'This view olny accepts GET and POST methods'
        }

    else:  # Request method not POST
        return HttpResponse('This view only handles GET and POST request')

    return render(request, 'airpollution/welcome.html', context)

def temp_country_creator(request):

    countries = {
        'Albania': 'AL',
        'Andorra': 'AD',
        'Austria': 'AT',
        'Belgium': 'BE',
        'Bosnia and Herzegovina': 'BA',
        'Bulgaria': 'BG',
        'Croatia': 'HR',
        'Cyprus': 'CY',
        'Czech Republic': 'CZ',
        'Dennmark': 'DK',
        'Estonia': 'EE',
        'Finland': 'FI',
        'France': 'FR',
        'Germany': 'DE',
        'Greece': 'GR',
        'Hungary': 'HU',
        'Iceland': 'IS',
        'Ireland': 'IE',
        'Italy': 'IT',
        'Kosovo under UNSCR 1244/99': 'XK',
        'Latvia': 'LV',
        'Lithuania': 'LT',
        'Luxembourg': 'LU',
        'Malta': 'MT',
        'Montenegro': 'ME',
        'Netherlands': 'NL',
        'Norway': 'NO',
        'Poland': 'PL',
        'Portugal': 'PT',
        'Romania': 'RO',
        'Serbia': 'RS',
        'Slovakia': 'SK',
        'Slovenia': 'SI',
        'Spain': 'ES',
        'Sweden': 'SE',
        'Switzerland': 'CH',
        'North Macedonia': 'MK',
        'Turkey': 'TR',
        'United Kingdom': 'GB',
    }

    to_insert = []
    for country_name, iso_code in countries.items():
        to_insert.append(Country(iso_code=iso_code, name=country_name))
    Country.objects.bulk_create(to_insert)

    context = {
        'app_name': request.resolver_match.app_name,
        'message_success': 'Countries created successfully'
    }

    return render(request, 'airpollution/welcome.html', context)


