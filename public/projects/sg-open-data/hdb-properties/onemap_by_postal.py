
import time
import json
import itertools
import os.path as path
from onemap_api import searchStreet
import pandas as pd

if __name__ == '__main__':
    '''
        Postal code district list is from [URA](https://www.ura.gov.sg/realEstateIIWeb/resources/misc/list_of_postal_districts.htm).
        The page is not static, so requests + BS4 does not work.
        I can't be bothered to set up Selenium yet to scrap just a single small table on a single page, so here we are.
        There are currently 81 postal sectors so it may not be too wrong to just do a brute force iteration.
    '''
    thisdir = path.relpath(path.dirname(path.realpath(__file__)))
    getdir = lambda f: path.join(thisdir, f)
    with open(getdir('district_table.html'), 'rt') as f:
        pss = pd.read_html(io=f, header=[0])[0].iloc[:,1].str.replace(r'\s','',regex=True).str.split(',').aggregate('sum')
    bldgs = list(map(''.join,itertools.product(list(map(str,range(10))),list(map(str,range(10))))))
    for ps in pss:
        for bg in bldgs:
            s = ps + bg + '??'
            try:
                print('[{0}] Searching for: {1}'.format(time.ctime(time.time()), s))
            except OverflowError as e:
                print('Searching for: {}'.format(s))
            new_results = searchStreet(street=s)
            with open(getdir('onemap_addresses_postal.json'), 'at') as f:
                for r in new_results:
                    f.write(json.dumps(r))
                    f.write('\n')
