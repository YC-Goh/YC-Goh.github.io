
import pandas as pd
import json
from _001_base import *

def parse_affixes(input_folder: Path) -> dict:
    sheets = pd.read_excel(input_folder.joinpath("affix.xlsx"), sheet_name=None)
    rules = sheets["Advanced Options"]
    AFFIX_OPTIONS_COLS = [col for col in rules.columns if col.startswith(("affix_group_", ))]
    rules = rules.merge(
        rules
        .loc[lambda df: df["option"].isin(["Use Group"])]
        .dropna(subset=AFFIX_OPTIONS_COLS, how="all")
        [["slot"]], 
        on=["slot"], how="inner", validate="m:1"
    )
    rules = {
        g: gdf.drop(columns=["slot"]).set_index(keys=["option"], append=False).dropna(how="all", axis=1).to_dict(orient="dict") 
        for g, gdf in rules.groupby(by="slot", as_index=False)
    }
    for slot, affix_groups in rules.items():
        slot_sheet = sheets[slot]
        affix_groups = {group: rule for group, rule in affix_groups.items() if rule["Use Group"]}
        for group, rule in affix_groups.items():
            rule: dict
            rule.pop("Use Group")
            rule["affix_ids"] = slot_sheet.loc[lambda df: df[group].notna(), "id"].tolist()
        rules[slot] = affix_groups
    return rules

def main(input_folder: Path) -> dict:
    affixes = parse_affixes(input_folder)
    print(json.dumps(affixes, indent=2))
    return affixes

if __name__ == "__main__":
    rules = main(filepaths["filter_maker"]["input"])
