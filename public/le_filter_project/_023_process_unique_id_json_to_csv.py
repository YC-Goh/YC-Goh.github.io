
import pandas as pd
import json
from _001_base import *
from _022_process_unique_id_details import DETAILS_ORDER

GROUP_ORDER = [
    "Regular Unique Items", 
    "Weaver Unique Items", 
    "Set Items", 
]

def _deconstruct_id_dict(id_map: dict) -> list[dict]:
    id_list = []
    for unique_group, unique_by_id in id_map.items():
        for unique_id, unique_titles in unique_by_id.items():
            id_list.append({
                "group": unique_group, 
                "id": unique_id, 
                ** unique_titles, 
            })
    return id_list

def _deconstruct_details_dict(details_map: dict) -> list[dict]:
    details_list = []
    for unique_title, unique_details in details_map.items():
        details_list.append({"title": unique_title, **unique_details, })
    return details_list

def main() -> pd.DataFrame:
    id_dict = json.load(open(filepaths["unique_id"]["game_data"]["processed"].joinpath("unique_id.json"), "r"))
    id_dict = _deconstruct_id_dict(id_dict)
    id_frame = pd.DataFrame.from_records(id_dict)
    for col in ["group", "id", "title", "ilvl", "label"]:
        try:
            id_frame[col] = id_frame[col].str.strip().str.title()
        except:
            pass
    details_dict = json.load(open(filepaths["unique_id"]["details"]["processed"].joinpath("unique_details.json"), "r"))
    details_dict = _deconstruct_details_dict(details_dict)
    details_frame = pd.DataFrame.from_records(details_dict).reindex(columns=["title", *DETAILS_ORDER])
    for col in [
        "title", "type", "rarity", "subtype", "level", "class", "min_drop_level", 
        "lp_level", "lp0_pct", "lp1_pct", "lp2_pct", "lp3_pct", "lp4_pct", 
        "global_drop_reroll_chance", "rune_of_ascendance_chance", 
    ]:
        try:
            details_frame[col] = details_frame[col].str.strip().str.title()
        except:
            pass
    unique_frame = id_frame.merge(details_frame, on=["title"], how="outer", validate="m:m", indicator=True)
    unique_frame = unique_frame.drop(columns=["label", "ilvl", "_merge"])
    unique_frame["group"] = pd.Categorical(unique_frame["group"], GROUP_ORDER, ordered=True)
    unique_frame["type"] = pd.Categorical(unique_frame["type"], SLOT_ORDER_WITH_PRIMORDIAL, ordered=True)
    unique_frame = unique_frame.sort_values(by=["group", "type", "class", "lp_level", "global_drop_reroll_chance", "title"])
    return unique_frame

if __name__ == "__main__":
    df = main()
    df.to_csv(filepaths["unique_id"]["combined"].joinpath("unique.csv"), index=False, encoding="utf-8")
