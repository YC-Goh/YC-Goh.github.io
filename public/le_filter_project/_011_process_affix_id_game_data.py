
import json, re
import bs4 as bs
from _001_base import *

def _affix_id_html_parser(html_filepath: str) -> dict:
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
            div_entry_title = strip_ws(div_entry.get("title").strip()).title()
            div_entry_label = div_entry.find("div", attrs={"class": "checkbox-label"}).find_all("div")
            div_entry_label = [label_entry.get_text(" ", strip=True) for label_entry in div_entry_label]
            div_entry_label = [re.compile(r"\s+").sub(" ", label_entry).title() for label_entry in div_entry_label]
            div_entry_type = "\n".join(div_entry_label[-1:])
            div_entry_label = "\n".join(div_entry_label[:-1])
            div_data[div_entry_id] = {
                "title": div_entry_title, 
                "label": div_entry_label, 
                # "type": div_entry_type, 
            }
        categories_map[div_lab] = div_data
    return categories_map

def main() -> dict:
    category_map = dict()
    for item_slot_file in [
        "1h_axe.html", "1h_sword.html", "1h_mace.html", "1h_wand.html", "1h_dagger.html", "1h_sceptre.html", 
        "2h_axe.html", "2h_sword.html", "2h_mace.html", "2h_staff.html", "2h_spear.html", "2h_bow.html", 
        "catalyst.html", "shield.html", "quiver.html", 
        "helmet.html", "armour.html", "boots.html", "gloves.html", "belt.html", 
        "amulet.html", "ring.html", "relic.html", 
        "idol_small.html", "idol_minor.html", "idol_stout.html", "idol_humble.html", 
        "idol_grand.html", "idol_large.html", "idol_ornate.html", "idol_huge.html", "idol_adorned.html", 
    ]:
        html_filepath = filepaths["affix_id"]["game_data"]["raw"].joinpath(item_slot_file)
        item_slot = " ".join([part.strip().title() for part in item_slot_file.removesuffix(".html").split("_")])
        if item_slot.startswith(("Idol", )):
            item_slot = " ".join(item_slot.split(" ")[::-1])
        elif item_slot.startswith(("Armour", )):
            item_slot = "Body Armor"
        elif item_slot.endswith(("Dagger", "Sceptre", "Wand", "Bow", )):
            item_slot = item_slot.removeprefix("1H").removeprefix("2H").strip()
        elif item_slot.startswith(("1H", )):
            item_slot = item_slot.replace("1H", "One-Handed").strip()
        elif item_slot.startswith(("2H", )):
            item_slot = item_slot.replace("2H", "Two-Handed").strip()
        elif item_slot.endswith(("Catalyst", )):
            item_slot = f"Off-Hand {item_slot}".strip()
        category_map[item_slot] = _affix_id_html_parser(html_filepath)
    return category_map

if __name__ == "__main__":
    cat_map = main()
    # print(len(set([id for slot in cat_map.values() for group in slot.values() for id in group])))
    with open(filepaths["affix_id"]["game_data"]["processed"].joinpath("affix_id.json"), "wt") as outfile:
        outfile.write(json.dumps(cat_map, indent=2))
