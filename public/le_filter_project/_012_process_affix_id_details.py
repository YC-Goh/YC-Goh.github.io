
import json, re
import bs4 as bs
from _001_base import *

def _affix_details_html_parser(html_filepath: str) -> dict:
    soup = bs.BeautifulSoup(open(html_filepath, "rt"), features="html.parser")
    div_entry_list = soup.find_all("div", attrs={"class": "item-card"})
    div_entry_map = dict()
    for div_entry in div_entry_list:
        div_entry_description = div_entry.find("div", attrs={"class": "item-description"})
        div_entry_id = div_entry_description.find("a", attrs={"class": "item-name"})
        div_entry_name = strip_ws(div_entry_id.get_text(" ", strip=True)).title()
        if div_entry_id.has_attr("prefix-id"):
            div_entry_id = div_entry_id.get("prefix-id")
        elif div_entry_id.has_attr("suffix-id"):
            div_entry_id = div_entry_id.get("suffix-id")
        else:
            div_entry_id = div_entry_id.get("id")
        div_entry_tier_table = div_entry.find("div", attrs={"class": "tier-table"}).find_all("div", attrs={"class": "affix"})
        div_entry_tier_map = dict()
        for div_entry_tier in div_entry_tier_table:
            if div_entry_tier.has_attr("tier"):
                div_entry_tier_id = strip_ws(div_entry_tier.get("tier")).strip().title()
                div_entry_tier_range = div_entry_tier.find_all("div", attrs={"class": "affix-tier-range"})
                div_entry_tier_range = "\n".join([strip_ws(tier_range.get_text(" ", strip=True)).title() for tier_range in div_entry_tier_range])
                div_entry_tier_map[div_entry_tier_id] = div_entry_tier_range
        div_entry_applies_to = div_entry.find("ul", attrs={"class": "affix-applies-to-list"})
        if div_entry_applies_to:
            div_entry_applies_to = strip_ws(div_entry_applies_to.get_text(",", strip=True)).title()
            div_entry_applies_to = div_entry_applies_to.replace("\u00d7", "x")
        div_entry_level = div_entry.find("div", attrs={"class": "item-req"})
        if div_entry_level:
            div_entry_level = strip_ws(div_entry_level.get_text(" ", strip=True)).title()
            div_entry_level = div_entry_level.split(":")[1].strip()
            try:
                div_entry_level = int(div_entry_level)
            except:
                div_entry_level = int(float(div_entry_level))
        div_entry_class = div_entry.find("div", attrs={"class": "item-req2"})
        if div_entry_class:
            div_entry_class = strip_ws(div_entry_class.get_text(" ", strip=True)).title()
            div_entry_class = div_entry_class.split(":")[1].strip()
            div_entry_class = ",".join([req_class.strip() for req_class in div_entry_class.split("/")])
        div_entry_extra_info = div_entry.find_all("div", attrs={"class": "extra-info"})
        if div_entry_extra_info:
            div_entry_extra_info = "\n".join([strip_ws(extra_info.get_text(" ", strip=True)).title() for extra_info in div_entry_extra_info])
            div_entry_reroll_chance = re.compile(r"(?i)reroll\s+chance\W+(\d+\.?\d*)%").search(div_entry_extra_info)
            if div_entry_reroll_chance:
                div_entry_reroll_chance = div_entry_reroll_chance.group(1)
                try:
                    div_entry_reroll_chance = int(div_entry_reroll_chance)
                except:
                    div_entry_reroll_chance = int(float(div_entry_reroll_chance))
            div_entry_extra_info = re.compile(r"(?i)reroll\s+chance\W+(\d+\.?\d*)%").sub("", div_entry_extra_info).strip()
            div_entry_extra_info = re.compile(r"(?i)rarity.*(?:common|rare)").sub("", div_entry_extra_info).strip()
            div_entry_extra_info = strip_ws(div_entry_extra_info)
        div_entry_map[div_entry_id] = {
            "name": div_entry_name, 
            "tier_table": div_entry_tier_map, 
            "applies_to": div_entry_applies_to, 
            "level": div_entry_level, 
            "class": div_entry_class, 
            "reroll_chance": div_entry_reroll_chance, 
            "extra_info": div_entry_extra_info, 
        }
    return div_entry_map

def main() -> dict:
    prefix_filepath = filepaths["affix_id"]["details"]["raw"].joinpath("prefix.html")
    prefix_map = _affix_details_html_parser(prefix_filepath)
    suffix_filepath = filepaths["affix_id"]["details"]["raw"].joinpath("suffix.html")
    suffix_map = _affix_details_html_parser(suffix_filepath)
    category_map = {**prefix_map, **suffix_map}
    category_map = dict(sorted(category_map.items(), key=lambda item: item[1]["name"]))
    category_map = {i: val for i, (_, val) in enumerate(category_map.items())}
    return category_map

if __name__ == "__main__":
    cat_map = main()
    # print(json.dumps(cat_map, indent=2))
    with open(filepaths["affix_id"]["details"]["processed"].joinpath("affix_details.json"), "wt") as outfile:
        outfile.write(json.dumps(cat_map, indent=2))
