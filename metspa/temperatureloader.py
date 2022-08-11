import swagger_client
import pprint
import urllib.request
import os
import metspa.processdata as processdata
import logging


def load_api(API_KEY):
    configuration = swagger_client.Configuration()
    configuration.api_key['api_key'] = API_KEY

    api_instance = swagger_client.ValoresClimatologicosApi(swagger_client.ApiClient(configuration))

    return api_instance


def extract_aemet_data(data, start_year, end_year, idema):
    PROGRAM_DIRECTORY = data['program_directory']

    temp_json_data_directory = f'{PROGRAM_DIRECTORY}/temp_output/station_{idema}/'

    api_instance = load_api(data['api_key'])

    for year_ini in range(start_year, end_year+1, 4):
        if year_ini + 3 < end_year:
            year_last = year_ini + 3
        else:
            year_last = end_year
        logging.info(f'Getting values for start({year_ini}) to end({year_last})...')
        start_date = f"{year_ini}-01-01T00:00:00UTC"  # (AAAA-MM-DDTHH:MM:SSUTC)
        end_date = f"{year_last}-12-31T00:00:00UTC"  # (AAAA-MM-DDTHH:MM:SSUTC)

        if not os.path.isdir(temp_json_data_directory):
            os.makedirs(temp_json_data_directory)

        datafile = temp_json_data_directory + f'/climat{idema}_S{year_ini}_E{year_last}.json'

        if os.path.exists(datafile):
            logging.info('AEMET Data found for current period. To refresh clear temp directory with '
                         '`metspa clean`.')
            continue

        try:
            api_response = api_instance.climatologas_diarias_(start_date, end_date, idema)
            pprint.pprint(api_response)
        except swagger_client.rest.ApiException as e:
            print(e)
        except ValueError as e:
            print(e)
        else:
            contents = urllib.request.urlopen(api_response.datos).read()
            with open(datafile, 'wb') as fid:
                fid.write(contents)

    processdata.clean_data_from_multiple_json(temp_json_data_directory, data['output_directory'], idema)
