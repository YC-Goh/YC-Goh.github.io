
#%%

'''
    Going to be a huge pain to have to keep re-searching for datasets on the open data portal
    So just download it once and save it to search locally
'''

import requests
import time
import pandas as pd
import os

#%%

def main(sleep_interval:float=0.1, save_folder:str|None=None):
    '''
        Simple function.
        Loops over pages of the data.gov.sg datasets API until there are no more pages to riff through.
        At each page, check that the return code is OK or retry until OK (really ought to add max_tries later)
        and then if return code is OK, extract the datasets list to append to the master list.
        Finally convert the master list to a dataframe and export.

        This function must succeed in one pass.
        Luckily the datasets listing is not too large.
        For an interruptible function, the function can be revised the following way:
        1.  At each successful page load, save current extractions and the current page state 
            to a JSON file in the save folder.
        2.  Take an input (default to True) for whether to remove intermediate outputs from save folder
            once final full datasets listing is successfully exported.

    '''
    assert isinstance(sleep_interval, (float, int)), 'Sleep interval should be some kind of number'
    assert sleep_interval > 0.0, 'Sleep interval should be a positive number'
    assert sleep_interval < 3600, 'Set something reasonable for sleep interval (3600s == 1h!)'
    assert save_folder is None or isinstance(save_folder, str), 'Convert the folder path to string if not None'
    datasets = list()
    page_num = 1
    max_pages = 1
    while page_num <= max_pages:
        resp = requests.get('https://api-production.data.gov.sg/v2/public/api/datasets', params={'page': page_num})
        if resp.status_code == 200:
            page_num += 1
            max_pages = max(max_pages, resp.json()['data']['pages'])
            datasets = [*datasets, *resp.json()['data']['datasets']]
            print('Extracted %s dataset records.' % len(datasets))
            time.sleep(sleep_interval)
        else:
            time.sleep(5 * sleep_interval)
    df_datasets = pd.DataFrame(datasets)
    if save_folder is not None:
        df_datasets.to_csv(os.path.join(save_folder, 'datasets.csv'), index=False, encoding='utf-8-sig')
    return df_datasets

#%%

if __name__ == '__main__':
    data = main(0.1, os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, 'data')))

#%%
