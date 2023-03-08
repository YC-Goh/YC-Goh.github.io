import time, requests, json

def searchStreet(street:str, delay:float=.01, fail_delay:float=60, error_log:str='onemap_error.json')->list:
    '''
        Use OneMap public API to search all addresses at a particular street.
        
        Parameters:
        street (required): the street name to use to search.

        This is actually misleading --- I call it a street as I would prefer to search by street name, but nothing stops users from also earching by postal code or the like.
        Internally, the OneMap API only has a single field to submit a search query that accepts any address part or a full address.

        delay (optional; default=0.01): time between calls.
        fail_delay (optional; default=60): time to pause execution in case of connection errors (may be OneMap complaining due to rate limitation).

        OneMap has a rate limit of 250 calls per minute.

        error_log (optional): where to print errors to.

        returns: a list of dictionary objects (JSON object) containing all addresses matching that street.
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
