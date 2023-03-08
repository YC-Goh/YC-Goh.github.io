
import requests
import tempfile
import zipfile
import time

def getDownload(url, extract_path='.', extract_list=None):
    '''
        Most download links in data.gov.sg are zip files containing the data sets and metadata.
        Therefore the procedure here assumes a zip file and asks for the list of files to extract.

        Parameters:
        url (string): the download link from data.gov.sg.
        extract_path (string; optional, default='.'): where to save extracted data sets.
        extract_list ([int]; optional): list of integers corresponding to position numbers of files to extract from the archive.

        If extract_list is not given, this function will run in interactive mode.
        After the zip file is downloaded the function will display a numbered list of archive members and their file sizes.
        It will request for a (list of) number(s) corresponding to the item number (not the file sizes) to extract.
        Requested archive members will be extracted and saved to extract_path.
    '''
    retry = True
    while retry:
        try:
            req = requests.get(url, stream=True)
            retry = False
        except ConnectionError as e:
            print('{0}: {1}'.format(type(e), e))
            print('Use ctrl+c to terminate this program. Otherwise, a reconnection will be attempted in 1 minute.')
            time.sleep(60)
        except Exception as e:
            raise e
    if req.status_code == 200:
        with tempfile.TemporaryFile() as tf:
            for chunk in req.iter_content(chunk_size=1024):
                tf.write(chunk)
            with zipfile.ZipFile(tf) as zf:
                for i, zff in enumerate(zf.infolist()):
                    print('{})'.format(i), zff.filename, '({})'.format(zff.file_size))
                if extract_list is None:
                    zffn = list(map(int,input('Choose the number(s) of the file(s) to extract. Separate numbers by commas and do not insert spaces:\n').split(',')))
                else:
                    print('Extracting:',*extract_list)
                    zffn = extract_list
                zffn = [zff.filename for i, zff in enumerate(zf.infolist()) if i in zffn]
                for zff in zffn:
                    zf.extract(zff, path=extract_path)

if __name__ == '__main__':
    #   Road names (for OneMap geocoding)
    getDownload(url='https://data.gov.sg/dataset/f5b9f708-c31b-4fcf-b580-a2ee8e67c1ea/download', extract_list=[2])
    #   HDB property listing
    getDownload(url='https://data.gov.sg/dataset/9dd41b9c-b7d7-405b-88f8-61b9ca9ba224/download', extract_list=[1])
    #   HDB resale price history
    getDownload(url='https://data.gov.sg/dataset/7a339d20-3c57-4b11-a695-9348adfd7614/download', extract_list=[1,2,3,4,5])
    #   URA dwelling unit count by property
    getDownload(url='https://data.gov.sg/dataset/becee961-7685-4ba5-a147-01abc7fcce6c/download', extract_list=[1])
    #   URA Sub Zones: One version of administrative boundaries
    getDownload(url='https://data.gov.sg/dataset/c754450d-ecbd-4b7d-8dc1-c07ee842c6d1/download', extract_list=[1])
