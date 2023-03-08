
import geopandas as gpd
from fiona.drvsupport import supported_drivers
import requests
import time
import json

def searchStreet(street, delay=.01, fail_delay=60, error_log='onemap_error.json'):
    '''
        Use OneMap public API to search all addresses at a particular street
        street (required): the street name to use to search
        delay (optional; default=0.01): time between calls
        fail_delay (optional; default=60): time to pause execution in case of connection errors (may be OneMap complaining due to rate limitation)

        OneMap has a rate limit of 250 calls per minute

        error_log (optional): where to print errors to

        returns: a list of dictionary objects (JSON object) containing all addresses matching that street
    '''
    page_num = 1
    has_result = True
    all_results = []
    while has_result:
        time.sleep(delay)
        try:
            req = requests.get(
                url='https://developers.onemap.sg/commonapi/search', 
                params={
                    'searchVal': street,
                    'returnGeom': 'Y',
                    'getAddrDetails': 'Y',
                    'pageNum': page_num
                })
            if req.status_code == 200:
                results = req.json()['results']
                all_results += results
                has_result = len(results) > 0
                page_num += 1
        except ConnectionError as e:
            print(e)
            with open(error_log, 'at') as f:
                f.write(json.dumps({
                    'error': '{0}: {1}'.format(type(e), e),
                    'search_string': street,
                    'page_num': page_num
                }))
                f.write('\n')
            time.sleep(fail_delay)
        except Exception as e:
            '''
                Ideally there should be a different handling here
                But in the absence of information about what the potential errors are we can just continue
            '''
            print(e)
            with open(error_log, 'at') as f:
                f.write(json.dumps({
                    'error': '{0}: {1}'.format(type(e), e),
                    'search_string': street,
                    'page_num': page_num
                }))
                f.write('\n')
            time.sleep(fail_delay)
    return all_results

if __name__ == '__main__':
    '''
        road-network.kml is from data.gov.sg
        Specifically: https://data.gov.sg/dataset/master-plan-2019-road-name-layer
    '''
    supported_drivers['LIBKML'] = 'rw'
    sgroad = gpd.read_file('road-network.kml')
    for s in sgroad['RD_NAME'].unique():
        try:
            print('[{0}] Searching for: {1}'.format(time.ctime(time.time()), s))
        except OverflowError as e:
            print('Searching for: {}'.format(s))
        new_results = searchStreet(street=s)
        with open('onemap_addresses.json', 'at') as f:
            for r in new_results:
                f.write(json.dumps(r))
                f.write('\n')
