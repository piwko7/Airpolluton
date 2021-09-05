class XLEHEADERS():
    COUNTRY = 'country'
    CITY = 'city'
    STATION_EOI_CODE = 'stationeoicode'
    STATION_NAME = 'stationname'
    AIR_POLLUTANT = 'airpollutant'
    AIR_POLLUTION_LEVEL = 'airpollutionlevel'
    TYPE = 'type'
    AREA = 'area'
    LONGITUDE = 'longitude'
    LATITUDE = 'latitude'
    ALTITUDE = 'altitude'

    choices = [COUNTRY, CITY, STATION_EOI_CODE, STATION_NAME, AIR_POLLUTANT, AIR_POLLUTION_LEVEL, TYPE, AREA,
               LONGITUDE, LATITUDE, ALTITUDE]


def get_headers_and_units(work_sheet):
    headers_row = None
    headers = {}
    units = ''

    # Get headers row
    for row in range(work_sheet.max_row + 1):
        cell = work_sheet['A'][row].value
        if isinstance(cell, str) and 'country' in cell.lower():
            headers_row = row
            break
    if headers_row is None:
        return None, None, None

    # Remembers headers positions

    for i in range(work_sheet.max_column):
        # iterate over capital letters from CSV ('A', 'B' ...)
        column = chr(i + 65)
        header = work_sheet[column][headers_row].value
        header = header.strip().replace('_', '').lower()

        # get units (Different in some year, 2014 vs 2016 ex.)
        if 'm3' in header:
            units_index = header.find('(') + 1
            for index in range(units_index, units_index+20):
                if header[index] == ')':
                    break
                units += header[index]
            continue
        elif 'unit' in header:
            units = work_sheet[column][headers_row + 1].value
            continue

        # Map headers with their indices
        for choice in XLEHEADERS.choices:
            if choice in header:
                headers[choice] = i
                break

    return headers_row, headers, units