
import geopandas as gpd
from fiona.drvsupport import supported_drivers
import time
import json
import os.path as path
from onemap_api import searchStreet

if __name__ == '__main__':
    '''
        road-network.kml is from data.gov.sg
        Specifically: https://data.gov.sg/dataset/master-plan-2019-road-name-layer
    '''
    thisdir = path.relpath(path.dirname(path.realpath(__file__)))
    getdir = lambda f: path.join(thisdir, f)
    supported_drivers['LIBKML'] = 'rw'
    sgroad = gpd.read_file(getdir('road-network.kml'))
    for s in sgroad['RD_NAME'].unique():
        try:
            print('[{0}] Searching for: {1}'.format(time.ctime(time.time()), s))
        except OverflowError as e:
            print('Searching for: {}'.format(s))
        new_results = searchStreet(street=s)
        with open(getdir('onemap_addresses_street_name.json'), 'at') as f:
            for r in new_results:
                f.write(json.dumps(r))
                f.write('\n')
