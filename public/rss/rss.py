# %%

import os
import requests
import pandas as pd
from typing import Optional
import xml.etree.ElementTree as ET
import json
from datetime import datetime
import unicodedata

#%%

#   Removed feeds until function below can support
'''
    Issue: Uses RDF format which is not supported by the current implementation.
    "Science": {
        "Science Magazine": {
            "url": "https://www.science.org/rss/news_current.xml",
            "url_root": "https://www.science.org/content/article"
        }, 
        "Nature": {
            "url": "https://www.nature.com/nature.rss",
            "url_root": "https://www.nature.com/articles"
        }, 
        "PNAS News": {
            "url": "https://www.pnas.org/action/showfeed?type=searchTopic&taxonomyCode=type&tagCode=news-feat",
            "url_root": "https://www.pnas.org"
        }, 
        "PNAS Opinion": {
            "url": "https://www.pnas.org/action/showfeed?type=searchTopic&taxonomyCode=type&tagCode=opinion",
            "url_root": "https://www.pnas.org"
        }, 
        "PNAS Perspective": {
            "url": "https://www.pnas.org/action/showfeed?type=searchTopic&taxonomyCode=type&tagCode=pers",
            "url_root": "https://www.pnas.org"
        }, 
        "PNAS Commentary": {
            "url": "https://www.pnas.org/action/showfeed?type=searchTopic&taxonomyCode=type&tagCode=comm",
            "url_root": "https://www.pnas.org"
        }, 
        "PNAS Editorial": {
            "url": "https://www.pnas.org/action/showfeed?type=searchTopic&taxonomyCode=type&tagCode=edit",
            "url_root": "https://www.pnas.org"
        }
    }
'''

# %%

def rss_to_dataframe(rss_url: str, url_root: Optional[str] = None) -> pd.DataFrame:
    """
    Loads an RSS feed from the given URL and returns its contents as a pandas DataFrame.

    Args:
        rss_url (str): The URL of the RSS feed to load.
        url_root (Optional[str]): If provided, this root will be removed from all URLs extracted from the feed.

    Returns:
        pd.DataFrame: DataFrame containing columns 'headline', 'url', and 'publish_date'.
    """
    response = requests.get(rss_url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:140.0) Gecko/20100101 Firefox/140.0'})

    # ET.fromstring parses XML content directly from the response
    # efficient for in-memory operations
    root = ET.fromstring(response.content)

    def parse_rss_item(item: ET.Element) -> Optional[dict]:
        title = item.find('title').text
        link = item.find('link').text

        # ternary operator handles cases where <pubDate> might be missing, preventing AttributeError
        pub_date = item.find('pubDate').text if item.find('pubDate') is not None else None

        # Removing url_root from the start of the link normalizes URLs for downstream processing or display
        if url_root and link.startswith(url_root):
            link = link[len(url_root):]

            return {
                'headline': title,
                'url': link,
                'publish_date': pub_date
            }
        
        else:
            return None

    # root.findall('.//item') captures all news items regardless of their nesting in the XML structure
    items = list(map(parse_rss_item, root.findall('.//item')))
    items = [item for item in items if item is not None]  # Filter out None values

    df = pd.DataFrame(items)
    try:
        df['publish_date'] = pd.to_datetime(df['publish_date'].str.replace(r'(?i)\s*[a-z](?:tc|dt|st|mt)$', '', regex=True))
    except:
        df['publish_date'] = pd.to_datetime(df['publish_date'].str.replace(r'(?i)\s*[a-z](?:tc|dt|st|mt)$', '', regex=True), dayfirst=True, format='mixed')

    # Split publish_date into separate date and time columns
    df['publish_time'] = df['publish_date'].dt.time
    df['publish_date'] = df['publish_date'].dt.date

    return df

#%%

def normalize_headline(headline: str) -> str:
    """
    Normalizes a headline by:
    1. Replacing non-ASCII punctuation with ASCII equivalents.
    2. Trimming whitespace (both trailing and in-between).
    3. Ensuring UTF-8 encoding.
    4. Converting to fully decomposed normalization form.

    Args:
        headline (str): The headline to normalize.

    Returns:
        str: The normalized headline.
    """
    # Replace non-ASCII punctuation with ASCII equivalents
    replacements = {
        '\u201C': '"',  # Replace left double quotation mark with standard quotes
        '\u201D': '"',  # Replace right double quotation mark with standard quotes
        '\u2013': '-',    # Replace en-dash with standard dash
        '\u2014': '-',    # Replace em-dash with standard dash
        '\u2018': "'",    # Replace left single quotation mark with standard single quote
        '\u2019': "'",    # Replace right single quotation mark with standard single quote
        '\u00A0': ' '     # Replace non-breaking space with standard space
    }

    for old, new in replacements.items():
        headline = headline.replace(old, new)

    # Trim whitespace (both trailing and in-between)
    headline = ' '.join(headline.split())

    # Ensure UTF-8 encoding and convert to fully decomposed normalization form
    headline = unicodedata.normalize('NFD', headline)

    return headline

#%%

def process_rss_feeds(json_file: str) -> pd.DataFrame:
    """
    Processes RSS feeds from a JSON file and saves the extracted data to a CSV file.
    The JSON file is assumed to be structured with topics as keys, each containing a dictionary of sites,
    where each site has a URL and an optional URL root.

    Args:
        json_file (str): Path to the JSON file containing RSS feed metadata.
        output_csv_prefix (str): Prefix for the output CSV file name.
    """
    # Find the path of current file
    rss_file_path = os.path.dirname(os.path.abspath(__file__))

    # Load RSS feed metadata from JSON file
    with open(os.path.join(rss_file_path, json_file), 'r') as f:
        rss_metadata: dict[str,dict[str,dict[str,str]]] = json.load(f)

    # Initialize an empty list to store dataframes
    all_dataframes = []

    # Iterate through topics and sites in the JSON structure
    for topic, sites in rss_metadata.items():
        for site, site_data in sites.items():
            rss_url = site_data.get('url')
            url_root = site_data.get('url_root')

            # Extract RSS feed data using rss_to_dataframe
            df = rss_to_dataframe(rss_url, url_root)

            # Add topic, site, and url_root columns to the dataframe
            df['topic'] = topic
            df['site'] = site
            df['url_root'] = url_root

            # Normalize the headline
            df['headline'] = df['headline'].apply(normalize_headline)

            # Copy the dataframe to avoid fragmentation
            df = df.copy()

            # Append the dataframe to the list
            all_dataframes.append(df)

    # Combine all dataframes into a single dataframe
    final_df = pd.concat(all_dataframes, ignore_index=True).copy()

    # Rearrange columns to ensure the desired order
    column_order = ['topic', 'site', 'url_root', 'headline', 'url', 'publish_date', 'publish_time']
    final_df = final_df[column_order].copy()

    return final_df

#%%

if __name__ == '__main__':
    final_df = process_rss_feeds('rss.json')
    print(f'Processed RSS feeds at {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}.')

    # Find the path of current file
    rss_file_path = os.path.dirname(os.path.abspath(__file__))

    # Generate the output file name with the current date
    current_date = datetime.now() - pd.Timedelta(hours=8) # Adjust for UTC+8 timezone
    current_date = current_date.strftime('%Y%m%d')
    output_csv = f'rss_{current_date}.csv'

    # Save the combined dataframe to a CSV file
    final_df.to_csv(os.path.join(rss_file_path, 'data', 'daily', output_csv), index=False)
    print(f'Saved headlines at {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}.')

# %%
