
import json, re
import bs4 as bs
from _001_base import *

LPX_RE = re.compile(r"(?i)(lp\d)")
XINY_RE = re.compile(r"(?i)(\d+\W*in\W*\d+(?:,\d+)*)")
INT_RE = re.compile(r"(?i)(\d+)")
PCT_RE = re.compile(r"(?i)(\d+(?:\.\d+)?(?:e\-\d+(?:\,d+)*)?%)")
DETAILS_ORDER = [
    "type", 
    "rarity", 
    "subtype", 
    "level", 
    "class", 
    "min_drop_level", 
    "implicit", 
    "explicit", 
    "lp_level", 
    "lp0_pct", 
    "lp1_pct", 
    "lp2_pct", 
    "lp3_pct", 
    "lp4_pct", 
    "lp_remarks", 
    "global_drop_reroll_chance", 
    "rune_of_ascendance_chance", 
    "vendor_cost", 
    "timeline", 
    "dungeon", 
    "arena", 
    "bossfight", 
    "related_ailments", 
    "related_abilities", 
    "lore", 
]

def _unique_details_html_parser(html_filepath: str) -> dict:
    soup = bs.BeautifulSoup(open(html_filepath, "rt"), features="html.parser")
    entry_list = soup.find_all("div", attrs={"class": "item-card"})
    entry_map = dict()
    for entry in entry_list:
        entry_description = entry.find("div", attrs={"class": "item-description"})

        entry_id = entry_description.find("a", attrs={"class": "item-name"})
        entry_id = strip_ws(" ".join(entry_id.stripped_strings))

        entry_type = entry_description.find("div", attrs={"class": "item-type"})
        entry_subtype = entry_type.find("a", attrs={"item-id": True})
        entry_subtype = list(entry_subtype.stripped_strings) if entry_subtype == entry_subtype and entry_subtype is not None else list()
        entry_type = list(entry_type.stripped_strings)
        entry_rarity = [entry for entry in entry_type if entry.upper().startswith(tuple(RARITY_ORDER))]
        entry_type = [entry for entry in entry_type if entry not in entry_rarity and entry not in entry_subtype]
        entry_type = strip_ws(" ".join(entry_type))
        entry_rarity = strip_ws(" ".join(entry_rarity))
        entry_subtype = strip_ws(" ".join(entry_subtype))

        entry_implicit_start = entry.find("div", attrs={"class": "implicits-title"})
        entry_implicit_mods = list()
        if entry_implicit_start == entry_implicit_start and entry_implicit_start is not None:
            implicit = entry_implicit_start.find_next_sibling("div")
            while implicit == implicit and implicit is not None and any(class_value in implicit.get("class") for class_value in ["item-mod-unique", ]):
                entry_implicit_mods.append(strip_ws(" ".join(implicit.stripped_strings)))
                implicit = implicit.find_next_sibling("div")
        entry_implicit_mods = "\n".join(entry_implicit_mods)

        entry_explicit_start = entry.find("div", attrs={"class": "modifiers-title"})
        entry_explicit_mods = list()
        if entry_explicit_start == entry_explicit_start and entry_explicit_start is not None:
            explicit = entry_explicit_start.find_next_sibling("div")
            while explicit == explicit and explicit is not None and any(class_value in explicit.get("class") for class_value in ["item-mod-unique", ]):
                entry_explicit_mods.append(strip_ws(" ".join(explicit.stripped_strings)))
                explicit = explicit.find_next_sibling("div")
        entry_explicit_mods = "\n".join(entry_explicit_mods)

        entry_level = entry.find("div", attrs={"class": "item-req"})
        if entry_level == entry_level and entry_level is not None:
            entry_level = strip_ws(" ".join(entry_level.stripped_strings))
            entry_level = INT_RE.search(entry_level).group(1)
        else:
            entry_level = None

        entry_req = entry.find_all("div", attrs={"class": "item-req2"})
        entry_class = None
        entry_min_drop_level = None
        if entry_req == entry_req and entry_req is not None:
            for entry_req_item in entry_req:
                if "Class" in " ".join(entry_req_item.stripped_strings):
                    entry_class = strip_ws(" ".join([text for span in entry_req_item.find_all("span") for text in span.stripped_strings]))
                elif "Drop Level" in " ".join(entry_req_item.stripped_strings):
                    entry_min_drop_level = strip_ws(" ".join([text for span in entry_req_item.find_all("span") for text in span.stripped_strings]))

        entry_lp = entry.find_all("div", attrs={"class": "legendary-potential"})
        entry_lp_lpl = list()
        entry_lp_lpc = list()
        entry_lp_remarks = list()
        for entry_lp_item in entry_lp:
            entry_lp_item_find = entry_lp_item.find("span", attrs={"class": "lpl"})
            if entry_lp_item_find == entry_lp_item_find and entry_lp_item_find is not None:
                entry_lp_lpl.append(strip_ws(" ".join(entry_lp_item_find.stripped_strings)))
                for entry_lp_item_find in entry_lp_item.find_all("li"):
                    entry_lp_lpc.append(list(entry_lp_item_find.stripped_strings))
            else:
                entry_lp_remarks.append(strip_ws(" ".join(entry_lp_item.find("div", attrs={"class": "title"}).stripped_strings)))
        if len(entry_lp_lpc) > 0:
            entry_lp_lpc = {
                LPX_RE.search(entry[0]).group(1): (
                    XINY_RE.search(entry[1]), 
                    PCT_RE.search(entry[2]), 
                ) 
                for entry in entry_lp_lpc
            }
            entry_lp_lpc = {key: (entry_odds.group(1) if entry_odds else None, entry_pct.group(1) if entry_pct else None) for key, (entry_odds, entry_pct) in entry_lp_lpc.items()}
        else:
            entry_lp_lpc = {f"LP{i}": (None, None,) for i in range(0, 5, 1)}
        entry_lp_lpl = "\n".join(entry_lp_lpl)
        entry_lp_remarks = "\n".join(entry_lp_remarks)

        entry_dropfrom = entry.find("div", attrs={"class": "dropped-from"})
        entry_drop_globaldrop = list()
        entry_drop_crafting = list()
        entry_drop_vendor = list()
        entry_drop_timeline = list()
        entry_drop_dungeon = list()
        entry_drop_arena = list()
        entry_drop_bossfight = list()
        if entry_dropfrom == entry_dropfrom and entry_dropfrom is not None:
            for drop_entry in entry_dropfrom.find_all("li"):
                if drop_entry.find("span", attrs={"class": "random-drop"}) is not None:
                    drop_entry = [entry for entry in drop_entry.stripped_strings if entry.startswith(("Reroll Chance", ))]
                    entry_drop_globaldrop.append(strip_ws(" ".join([PCT_RE.search(entry).group(1) for entry in drop_entry])))
                elif drop_entry.find("span", attrs={"class": "item-crafting"}) is not None:
                    drop_entry = [entry for entry in drop_entry.stripped_strings if entry.endswith(("chance", ))]
                    entry_drop_crafting.append(strip_ws(" ".join([PCT_RE.search(entry).group(1) for entry in drop_entry])))
                elif drop_entry.find("span", attrs={"class": "npc-name"}) is not None:
                    drop_entry = (
                        strip_ws(" ".join(list(drop_entry.find("span", attrs={"class": "npc-name"}).stripped_strings))), 
                        "\n".join([
                            strip_ws(" ".join(entry.stripped_strings)) 
                            for entry in drop_entry.find("div", attrs={"class": "vendor-cost"}).find_all("div")
                        ]), 
                    )
                    entry_drop_vendor.append("\n".join(drop_entry))
                elif drop_entry.find("a", attrs={"class": "timeline"}) is not None:
                    entry_drop_timeline.append(strip_ws(" ".join(drop_entry.stripped_strings)))
                elif drop_entry.find("a", attrs={"class": "dungeon"}) is not None:
                    entry_drop_dungeon.append(strip_ws(" ".join(drop_entry.stripped_strings)).replace(" Tier", "\nTier"))
                elif drop_entry.find("a", attrs={"class": "arena"}) is not None:
                    entry_drop_arena.append(strip_ws(" ".join(drop_entry.stripped_strings)).replace(" Tier", "\nTier").replace(" Endless", "\nEndless"))
                else:
                    entry_drop_bossfight.append(strip_ws(" ".join(drop_entry.stripped_strings)))
        entry_drop_globaldrop = "\n".join(entry_drop_globaldrop)
        entry_drop_crafting = "\n".join(entry_drop_crafting)
        entry_drop_vendor = "\n".join(entry_drop_vendor)
        entry_drop_timeline = "\n".join(entry_drop_timeline)
        entry_drop_dungeon = "\n".join(entry_drop_dungeon)
        entry_drop_arena = "\n".join(entry_drop_arena)
        entry_drop_bossfight = "\n".join(entry_drop_bossfight)

        entry_related = entry.find_all("div", attrs={"class": "related-refs"})
        entry_rel_ailment = list()
        entry_rel_ability = list()
        if entry_related == entry_related and entry_related is not None:
            for entry_rel_item in entry_related:
                for entry_item in entry_rel_item.find_all("div", attrs={"class": "ailment-icon-name"}):
                    entry_rel_ailment.append(strip_ws(" ".join(entry_item.stripped_strings)))
                for entry_item in entry_rel_item.find_all("div", attrs={"class": "ability-icon-name"}):
                    entry_rel_ability.append(strip_ws(" ".join(entry_item.stripped_strings)))
        entry_rel_ailment = "\n".join(entry_rel_ailment)
        entry_rel_ability = "\n".join(entry_rel_ability)

        entry_lore = entry.find("div", attrs={"class": "item-lore"})
        if entry_lore == entry_lore and entry_lore is not None:
            entry_lore = strip_ws(" ".join(entry_lore.stripped_strings))
        else:
            entry_lore = None

        entry_map[entry_id] = dict()
        for key, val in zip(DETAILS_ORDER, [
            entry_type, 
            entry_rarity, 
            entry_subtype, 
            entry_level, 
            entry_class, 
            entry_min_drop_level, 
            entry_implicit_mods, 
            entry_explicit_mods, 
            entry_lp_lpl, 
            entry_lp_lpc["LP0"][1], 
            entry_lp_lpc["LP1"][1], 
            entry_lp_lpc["LP2"][1], 
            entry_lp_lpc["LP3"][1], 
            entry_lp_lpc["LP4"][1], 
            entry_lp_remarks, 
            entry_drop_globaldrop, 
            entry_drop_crafting, 
            entry_drop_vendor, 
            entry_drop_timeline, 
            entry_drop_dungeon, 
            entry_drop_arena, 
            entry_drop_bossfight, 
            entry_rel_ailment, 
            entry_rel_ability, 
            entry_lore, 
        ]):
            if val == val and val is not None and val not in ["", "?", ]:
                entry_map[entry_id][key] = val
    return entry_map

def main() -> dict:
    category_filepath = filepaths["unique_id"]["details"]["raw"].joinpath("all.html")
    category_map = _unique_details_html_parser(category_filepath)
    return category_map

if __name__ == "__main__":
    cat_map = main()
    # print(json.dumps(cat_map, indent=2))
    with open(filepaths["unique_id"]["details"]["processed"].joinpath("unique_details.json"), "wt") as outfile:
        outfile.write(json.dumps(cat_map, indent=2))
