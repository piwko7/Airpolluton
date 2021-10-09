import random

import openpyxl

work_book = openpyxl.load_workbook(filename='Kolory.xlsx')
sheet = work_book.active
color_list = []
for row in range(sheet.max_row):
    cell = sheet['B'][row].value
    color_list.append(cell)

random_list = random.sample(color_list, 39)  # 39 - number of countries
print(random_list)

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

for count, country in enumerate(countries):
    countries[country] = [countries[country], random_list[count]]

print(countries)

country_2 = {'Albania': ['AL', '#CD6600'],
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
