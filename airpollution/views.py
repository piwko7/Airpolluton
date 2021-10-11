import colorsys
import json

from django.contrib import messages
from django.db.models import Sum, Q, Max, Min
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django import forms
import openpyxl

from .models import Pollutant, Country, PollutantEntry
from .helpers import get_headers_and_units, XLEHEADERS

# Create your views here.

# from .models import


class ExcelUploadForm(forms.Form):
    year = forms.CharField(max_length=4)
    file = forms.FileField()


def upload(request):
    if request.method == 'GET':
        pass

    elif request.method == 'POST':

        form = ExcelUploadForm(request.POST, request.FILES)
        print(form.is_valid())
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
            messages.success(request, 'File uploaded successfully!')
        else:
            messages.warning(request, 'Complete the form correctly!')

    else:
        return HttpResponse('This view only handles GET and POST request')

    return render(request, 'airpollution/upload.html')

def table(request):
    return render(request, 'airpollution/table.html')


def charts(request):
    context = {
        'pollutant_list': [p.name for p in Pollutant.objects.all()]
    }

    return render(request, 'airpollution/charts.html', context)

def airpollution_table_data(request):
    table_data = {}
    pollutant_list = [pollutant for pollutant in Pollutant.objects.all()]
    country_list = [country for country in Country.objects.all()]

    for pollutant in pollutant_list:
        table_data[pollutant.name] = {}

        for i, country in enumerate(country_list):
            total = PollutantEntry.objects \
                .aggregate(total=Sum('pollution_level', filter=Q(pollutant=pollutant,
                                                                 country=country)))['total']
            minimum = PollutantEntry.objects \
                .aggregate(min=Min('pollution_level', filter=Q(pollutant=pollutant,
                                                               country=country)))['min']

            maximum = PollutantEntry.objects \
                .aggregate(max=Max('pollution_level', filter=Q(pollutant=pollutant,
                                                               country=country)))['max']

            count = PollutantEntry.objects.filter(pollutant=pollutant, country=country).count()
            units = PollutantEntry.objects.filter(pollutant=pollutant, country=country).first()
            units = units.units if units else ''
            if total is not None and count:
                table_data[pollutant.name][country.iso_code] = {'avg': total / count, 'min': minimum,
                                                                'max': maximum, 'limit': pollutant.limit_value,
                                                                'units': units}
    return JsonResponse(table_data)


def airpollution_visual_data_1(request):
    visuals_data = {'Pollution Levels by Pollutant by Country': {
        'chart_type': 'chart1',
        'labels': [],
        'datasets': [
            {
                'label': 'Limit',
                'backgroundColor': '#3C9C85',
                'stack': 'limit',
                'data': []}
        ]
    },
    }
    pollutant_list = [pollutant for pollutant in Pollutant.objects.all()]
    country_list = [country for country in Country.objects.all()]
    visuals_data['Pollution Levels by Pollutant by Country']['datasets'] += \
        [{'label': c.name, 'backgroundColor': c.color, 'hidden': 'true', 'data': []} for c in country_list]

    # populate data from DB
    for pollutant in pollutant_list:
        visuals_data['Pollution Levels by Pollutant by Country']['labels'].append(pollutant.name)
        visuals_data['Pollution Levels by Pollutant by Country']['datasets'][0]['data'].append(pollutant.limit_value)
        for i, country in enumerate(country_list):
            total = PollutantEntry.objects \
                .aggregate(total=Sum('pollution_level', filter=Q(pollutant=pollutant,
                                                                 country=country)))['total']

            count = PollutantEntry.objects.filter(pollutant=pollutant, country=country).count()
            if total is not None and count:
                visuals_data['Pollution Levels by Pollutant by Country']['datasets'][i + 1]['data'] \
                    .append(round(total / count, 2))
            else:
                # in case if total not egsist
                visuals_data['Pollution Levels by Pollutant by Country']['datasets'][i + 1]['data'].append(-1)

    return JsonResponse(visuals_data)

def airpollution_visual_data_2(request):

    pollutant_name = request.GET.get('pollutant', 'PM10')
    pollutant = Pollutant.objects.get(name=pollutant_name)
    summary_type = request.GET.get('summary_type', 'max')
    if summary_type == 'avg':
        name_prefix = 'Avarage'
    elif summary_type == 'min':
        name_prefix = 'Minimum'
    else: # by default -> max
        name_prefix = 'Maximum'

    all_years = [pe['year'] for pe in PollutantEntry.objects.order_by('year').values('year').distinct()]
    all_counries = list(Country.objects.all())
    all_pollutants = [p.name for p in Pollutant.objects.all()]
    visuals_data = {
        'name': f'{name_prefix} pollution level by country over time',
        'labels': all_years,
        'datasets': [
            {'label': 'Limit',
             'borderColor': '#3C9C85',
             'backgroundColor': '#3C9C85',
             'data': [pollutant.limit_value] * len(all_years),
             'fill': False,
             },
        ]
    }

    for country in all_counries:
        country_data = {'label': country.name,
                        'borderColor': country.color,
                        'backgroundColor': country.color,
                        'data': [],
                        'fill': False,
                        'hidden': True
                        }
        visuals_data['datasets'].append(country_data)

        for year in all_years:
            f = Q(pollutant=pollutant, year=year, country=country)
            if summary_type == 'avg':
                country_tot = PollutantEntry.objects.aggregate(s=Sum('pollution_level', filter=f))['s']
                country_count = PollutantEntry.objects.filter(f).count()
                country_data['data'].append(country_tot / country_count if country_count else 0)
            elif summary_type == 'min':
                country_min = PollutantEntry.objects.aggregate(s=Min('pollution_level', filter=f))['s']
                country_data['data'].append(country_min if country_min else 0)
            else: # by def -> max
                country_max = PollutantEntry.objects.aggregate(s=Max('pollution_level', filter=f))['s']
                country_data['data'].append(country_max if country_max else 0)


    return JsonResponse(visuals_data)


def temp_country_creator(request):

    countries = {'Albania': ['AL', '#CD6600'],
                 'Andorra': ['AD', '#C71585'],
                 'Austria': ['AT', '#FDF5E6'],
                 'Belgium': ['BE', '#5E5E5E'],
                 'Bosnia and Herzegovina': ['BA', '#9ACD32'],
                 'Bulgaria': ['BG', '#EEEEE0'],
                 'Croatia': ['HR', '#CDC0B0'],
                 'Cyprus': ['CY', '#8A2BE2'],
                 'Czech Republic': ['CZ', '#BFBFBF'],
                 'Dennmark': ['DK', '#EEEED1'],
                 'Estonia': ['EE', '#9B30FF'],
                 'Finland': ['FI', '#7D9EC0'],
                 'France': ['FR', '#EEE8CD'],
                 'Germany': ['DE', '#EDEDED'],
                 'Greece': ['GR', '#4D4D4D'],
                 'Hungary': ['HU', '#8B1A1A'],
                 'Iceland': ['IS', '#CD3700'],
                 'Ireland': ['IE', '#7FFF00'],
                 'Italy': ['IT', '#708090'],
                 'Kosovo under UNSCR 1244/99': ['XK', '#6959CD'],
                 'Latvia': ['LV', '#8E8E8E'],
                 'Lithuania': ['LT', '#DAA520'],
                 'Luxembourg': ['LU', '#292929'],
                 'Malta': ['MT', '#D3D3D3'],
                 'Montenegro': ['ME', '#03A89E'],
                 'Netherlands': ['NL', '#9400D3'],
                 'Norway': ['NO', '#8B8878'],
                 'Poland': ['PL', '#1E1E1E'],
                 'Portugal': ['PT', '#8B8386'],
                 'Romania': ['RO', '#B4CDCD'],
                 'Serbia': ['RS', '#7CCD7C'],
                 'Slovakia': ['SK', '#F0E68C'],
                 'Slovenia': ['SI', '#66CDAA'],
                 'Spain': ['ES', '#CD2990'],
                 'Sweden': ['SE', '#525252'],
                 'Switzerland': ['CH', '#8B475D'],
                 'North Macedonia': ['MK', '#1C1C1C'],
                 'Turkey': ['TR', '#FAF0E6'],
                 'United Kingdom': ['GB', '#EE30A7']
                 }

    to_insert = []
    for country_name, data in countries.items():
        to_insert.append(Country(iso_code=data[0], name=country_name, color=data[1]))

    if request.GET.get('update', '') == 'true':
        Country.objects.bulk_update(to_insert, ['color'])
    else:
        Country.objects.bulk_create(to_insert)

    Country.objects.bulk_create(to_insert)

    context = {
        'message_success': 'Countries created successfully'
    }

    return render(request, 'airpollution/welcome.html', context)


def temp_add_colors_to_pollutants(request):
    try:
        pollutants = ['PM2.5', 'PM10', 'NO2', '03', 'BaP', 'S02']
        colors = ['#dccc', '#dccdb', '#5c63dc', '#5cdadc', '#66dc5c', '#dcdb5c']
        to_insert = [Pollutant(name=pollutant, color=colors[i]) for i, pollutant in enumerate(pollutants)]
        Pollutant.objects.bulk_update(to_insert, ['color'])
        messages.success(request, 'Colors added successfully!')
    except Exception as e:
        messages.error(request, e)

    return redirect('airpollution:upload')


