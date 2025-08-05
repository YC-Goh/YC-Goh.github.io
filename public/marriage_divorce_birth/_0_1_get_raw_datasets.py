
#%%

from core import *
import requests, json

#%%

def _return_records_datagovsg(dataset_id: str) -> dict:
    """
        This returns the records part of a dataset at data.gov.sg.
        The return format is relatively standardised across all datasets in data.gov.sg,
        so the 
    """
    response = requests.get(
        'https://data.gov.sg/api/action/datastore_search', 
        params={
            'resource_id': dataset_id,
            'limit': 999
        }
    )
    data = response.json()
    records = data['result']['records']
    return records

#%%

def _flatten_json(json_obj: dict, prefix: dict = None) -> dict[str, str]:
    flat_json = dict()
    for key, val in json_obj.items():
        if prefix is None:
            fullkey = key[:]
        else:
            fullkey = f'{prefix}_{key}'
        if isinstance(val, dict):
            for subkey, subval in _flatten_json(val, fullkey).items():
                flat_json[subkey] = subval
        else:
            flat_json[fullkey] = val
    return flat_json

#%%



#%%

if __name__ == '__main__':
    dataset_id = json.load(open(os.path.join(project_directories['root_marriage'], '_0_1_dataset_ids.json'), 'rb'))
    for set_name, set_id in _flatten_json(dataset_id).items():
        set_records = _return_records_datagovsg(set_id)
        with open(os.path.join(project_directories['root_marriage'], 'raw', f'{set_name}.json'), 'wt') as jsonfile:
            json.dump(set_records, jsonfile, indent=2)

#%%
