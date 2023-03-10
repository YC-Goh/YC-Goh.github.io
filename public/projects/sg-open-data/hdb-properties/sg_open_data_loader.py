import pandas as pd
import geopandas as gpd
import fiona

def getDataInFrame(filename:str, tolower:bool=True, todrop:list=None, dropduplicatesby:list=None)->pd.DataFrame:
    ext = filename.rsplit('.', maxsplit=1)[-1]
    fileloc = './hdb-properties/{}'.format(filename)
    if ext == 'json':
        try:
            df = pd.read_json(fileloc, encoding='utf-8')
        except ValueError as e:
            df = pd.read_json(fileloc, encoding='utf-8', lines=True)
        except Exception as e:
            raise e
    elif ext == 'csv':
        try:
            df = pd.read_csv(fileloc, encoding='utf-8')
        except Exception as e:
            raise e
    elif ext == 'kml':
        fiona.drvsupport.supported_drivers['LIBKML'] = 'rw'
        df = gpd.read_file(fileloc, driver='LIBKML')
        df = df.drop(columns=['description'])
    if tolower:
        df = df.rename(columns=dict(zip(df.columns,df.columns.str.lower())))
        if todrop is not None:
            todrop = [c.lower() if isinstance(c, str) else c for c in todrop]
        if dropduplicatesby is not None:
            dropduplicatesby = [c.lower() if isinstance(c, str) else c for c in dropduplicatesby]
    if todrop is not None:
        df = df.drop(columns=todrop)
    if dropduplicatesby is not None:
        df = df.drop_duplicates(subset=dropduplicatesby, keep='first')
    return df