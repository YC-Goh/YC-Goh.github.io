
import json, re
import bs4 as bs
from _001_base import *

def _unique_id_html_parser(html_filepath: str) -> dict:
    soup = bs.BeautifulSoup(open(html_filepath, "rt"), features="html.parser")
    categories = soup.find_all("div", attrs={"class": "category-header"})
    categories_map = dict()
    for div in categories:
        div_lab = div.find("div", attrs={"class": "checkbox-label"})
        div_lab = div_lab.get_text("", strip=True)
        div_entry_list = div.find_next_sibling("div", attrs={"class": "category-contents"}).find_all("div", attrs={"class": "category-entry"})
        div_data = dict()
        for div_entry in div_entry_list:
            div_entry_id = strip_ws(div_entry.get("entry-id").strip())
            div_entry_title = strip_ws(div_entry.get("data-search").strip())
            div_entry_label = div_entry.find("div", attrs={"class": "checkbox-label"}).find_all("div")
            div_entry_ilvl = [label_entry.find("span", attrs={"class": "entry-ilvl"}).get_text(" ", strip=True) for label_entry in div_entry_label]
            div_entry_label = [label_entry.get_text(" ", strip=True) for label_entry in div_entry_label]
            div_entry_ilvl = "\n".join(div_entry_ilvl)
            div_entry_label = "\n".join(div_entry_label)
            div_entry_title = div_entry_title.replace(div_entry_ilvl, "").strip()
            div_entry_ilvl = re.compile(r"(\d+)").search(div_entry_ilvl).group(1)
            div_data[div_entry_id] = {
                "title": div_entry_title, 
                "label": div_entry_label, 
                "ilvl": div_entry_ilvl, 
                # "type": div_entry_type, 
            }
        categories_map[div_lab] = div_data
    return categories_map

def main() -> dict:
    category_map = dict()
    html_filepath = filepaths["unique_id"]["game_data"]["raw"].joinpath("all.html")
    category_map = _unique_id_html_parser(html_filepath)
    return category_map

if __name__ == "__main__":
    cat_map = main()
    with open(filepaths["unique_id"]["game_data"]["processed"].joinpath("unique_id.json"), "wt") as outfile:
        outfile.write(json.dumps(cat_map, indent=2))
