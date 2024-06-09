
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

class DatasetsList():

    dataset_list_api = ''
    dataset_data_api = 'https://data.gov.sg/api/action/datastore_search'
    loaded_data:dict[str,pd.DataFrame] = dict()

    def __init__(self, datasets_location:str):
        self.datasets = pd.read_csv(datasets_location, index_col=['datasetId'])
    
    def search(self, search_list:list[str], invert:bool|list[bool]=False, regex:bool|list[bool]=True):
        if isinstance(invert, bool):
            invert = [invert] * len(search_list)
        if isinstance(regex, bool):
            regex = [regex] * len(search_list)
        mask = None
        for search_term, term_invert, term_regex in zip(search_list, invert, regex):
            term_mask = self.datasets['name'].str.contains(search_term, regex=term_regex)
            if term_invert:
                term_mask = ~term_mask
            if mask is None:
                mask = term_mask
            else:
                mask = mask&term_mask
        if mask is None:
            mask = pd.Series([True] * self.datasets.index.size)
        return self.datasets.loc[mask,'name'].to_dict()
    
    def _try_request(self, url:str, params:dict, max_tries:int=5):
        for _ in range(max_tries):
            resp = requests.get(url, params=params)
            if resp.status_code == 200:
                return resp
            else:
                for _ in range(int(1e6)):
                    pass
        raise ConnectionError()
    
    def retrieve_dataset(self, datasetid:str):
        '''
            To prevent repeatedly calling the API while testing reshaping data,
            instead save any datasets called in the session in state
            and simply return this dataset whenever the same ID is requested again.
        '''
        if datasetid in self.loaded_data.keys():
            return self.loaded_data[datasetid]
        else:
            data = list()
            has_new_data = True
            offset = 0
            limit = 1000
            while has_new_data:
                try:
                    resp = self._try_request(self.dataset_data_api, {'resource_id': datasetid, 'offset': offset, 'limit': limit})
                except ConnectionError:
                    raise ConnectionError(f'Could not get a success response from {self.dataset_data_api} for key {datasetid}.')
                except Exception as e:
                    raise e
                if len(resp.json()['result']['records']) > 0:
                    data = [*data, *resp.json()['result']['records']]
                    offset += 1000
                else:
                    has_new_data = False
            data = pd.DataFrame.from_records(data)
            def _to_numeric(series:pd.Series):
                try:
                    return pd.to_numeric(series, errors='raise', downcast='integer')
                except:
                    return series
            def _to_int(value:bool|str|float|int):
                try:
                    value = float(value)
                    if value == int(value):
                        return int(value)
                    else:
                        return value
                except:
                    return value
            data = data.apply(_to_numeric, axis=0)
            data = data.rename(columns=_to_int)
            data = data.rename(index=_to_int)
            self.loaded_data[datasetid] = data.copy(deep=True)
            return self.loaded_data[datasetid]

#%%
