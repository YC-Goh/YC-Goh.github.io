
import pandas as pd
import json
from _001_base import *

AFFIX_GROUPS = [f"affix_group_{n:.0f}" for n in range(6, 0, -1)]
AFFIX_ADVANCED_OPTIONS = ["Use Group", "Minimum Number of Affixes", "Minimum Tier", "Minimum Total Tier", ]
RULE_OPTIONS = ["Rule Description", "Recolour", "Sound", "Beam Colour", "Acolyte", "Primalist", "Mage", "Rogue", "Sentinel"]

SLOT_ORDER = [
    "One-Handed Axe", "One-Handed Mace", "One-Handed Sword", "Sceptre", "Dagger", "Wand", 
    "Two-Handed Axe", "Two-Handed Mace", "Two-Handed Sword", "Two-Handed Spear", "Two-Handed Staff", "Bow", 
    "Off-Hand Catalyst", "Shield", "Quiver", 
    "Helmet", "Body Armor", "Boots", "Gloves", "Belt", 
    "Ring", "Amulet", "Relic", 
    "Small Idol", "Minor Idol", "Humble Idol", "Stout Idol", 
    "Huge Idol", "Grand Idol", "Large Idol", "Ornate Idol", 
    "Adorned Idol", 
]
GROUP_ORDER = [
    "General Idols", "Acolyte Idols", "Primalist Idols", "Mage Idols", "Sentinel Idols", "Rogue Idols", "Weaver Idols", "Enchanted Idols", 
    "Attributes", 
    "Melee", "Bow", "Throwing", "Spell", "General", "Damage Type", 
    "Health", "Health Recovery", "Mana", "Potion", 
    "Resistance and Armor", "Ward", "Dodge", "Block", "Parry", "Leech", 
    "Stun", "Critical Strike Avoidance", 
    "Movement", "Cooldown", 
    "Minion", 
    "Ailments", 
    "Reflect", 
    "Acolyte", "Primalist", "Mage", "Sentinel", "Rogue", 
    "Personal", "Experimental", "Set", 
]

BASIC_FILTER_SLOTS = {
    f"{slot.lower().strip().replace(' ', '_')}_{i:.0f}": slot
    for slot in [*SLOT_ORDER, *META_SLOT_SELECTOR.keys()]
    for i in range(1, 4, 1)
}

def _deconstruct_id_dict(id_map: dict) -> list[dict]:
    id_list = []
    for slot, affix_by_group in id_map.items():
        for affix_group, affix_by_id in affix_by_group.items():
            for affix_id, affix_label in affix_by_id.items():
                id_list.append({
                    "slot": slot, 
                    "group": affix_group, 
                    "id": affix_id, 
                    ** affix_label
                })
    return id_list

def _deconstruct_details_dict(details_map: dict) -> list[dict]:
    details_list = []
    for _, affix_by_id in details_map.items():
        details_except_tier = {key: val for key, val in affix_by_id.items() if key not in ["tier_table"]}
        tier_details = {f"tier_{tier}": label for tier, label in affix_by_id["tier_table"].items()}
        details_list.append({**details_except_tier, **tier_details})
    return details_list

def _keep_row(row: pd.Series) -> bool:
    slot = row["slot"]
    applies_to = row["applies_to"]
    any_armour = ["Off-Hand Catalyst", "Shield", "Quiver", "Helmet", "Body Armor", "Boots", "Gloves", "Belt"]
    any_accessory = ["Amulet", "Ring", "Relic"]
    if applies_to == applies_to and applies_to:
        if (
            slot in applies_to.split(",") or
            slot in any_armour and "Any Armor" in applies_to.split(",") or 
            slot in any_accessory and "Any Accessory" in applies_to.split(",")
        ):
            return True
        else:
            return False
    else:
        return False

def _match_affix_type(gdf: pd.DataFrame) -> pd.Series:
    if gdf.index.size <= 1:
        return gdf.apply(lambda _: True, axis=1)
    else:
        label = gdf["label"]
        label_is_increased = label.str.contains(r"(?i)\b(?:increased?|chances?(?:\W*to|\W*for)?|speed)\b", regex=True, na=False)
        tier_1 = gdf["tier_1"]
        stat_is_increased = tier_1.str.contains(r"(?i)\d+(?:\.\d+)?\%", regex=True, na=False)
        return (
            (label_is_increased&stat_is_increased)|
            ((~label_is_increased)&(~stat_is_increased))
        )

def _match_affix_class(gdf: pd.DataFrame) -> pd.Series:
    if gdf.index.size <= 1:
        return gdf.apply(lambda _: True, axis=1)
    else:
        group = gdf["group"]
        group_is_idol = group.str.contains(r"(?i)\bidols?\b", regex=True, na=False)
        group_is_general = group.str.contains(r"(?i)\b(?:general|weaver)\b", regex=True, na=False)
        group_is_enchanted = group.str.contains(r"(?i)\benchante?d?\b", regex=True, na=False)
        group_is_not_class = ~group.str.contains(r"(?i)\b(?:sentinel|rogue|mage|acolyte|primalist)\b", regex=True, na=False)
        group_is_sentinel = group.str.contains(r"(?i)\bsentinel\b", regex=True, na=False)
        group_is_rogue = group.str.contains(r"(?i)\brogue\b", regex=True, na=False)
        group_is_mage = group.str.contains(r"(?i)\bmage\b", regex=True, na=False)
        group_is_acolyte = group.str.contains(r"(?i)\bacolyte\b", regex=True, na=False)
        group_is_primalist = group.str.contains(r"(?i)\bprimalist\b", regex=True, na=False)
        affix_class = gdf["class"]
        extra_info = gdf["extra_info"]
        class_is_general = affix_class.str.contains(r"(?i)\b(?:general|non\W+specific|all\W+classe?s?)\b", regex=True, na=True)
        class_is_enchanted = extra_info.str.contains(r"(?i)\benchante?d?.*affix.*class.*idols?\b", regex=True, na=False)
        class_is_sentinel = affix_class.str.contains(r"(?i)\bsentinel\b", regex=True, na=False)
        class_is_rogue = affix_class.str.contains(r"(?i)\brogue\b", regex=True, na=False)
        class_is_mage = affix_class.str.contains(r"(?i)\bmage\b", regex=True, na=False)
        class_is_acolyte = affix_class.str.contains(r"(?i)\bacolyte\b", regex=True, na=False)
        class_is_primalist = affix_class.str.contains(r"(?i)\bprimalist\b", regex=True, na=False)
        return (
            (group_is_idol&
                (
                    (group_is_general&class_is_general)|
                    (group_is_enchanted&class_is_enchanted)
                )
            )|
            (
                (group_is_not_class&class_is_general)|
                (group_is_sentinel&class_is_sentinel)|
                (group_is_rogue&class_is_rogue)|
                (group_is_mage&class_is_mage)|
                (group_is_acolyte&class_is_acolyte)|
                (group_is_primalist&class_is_primalist)
            )
        )

def instructions_sheet() -> pd.DataFrame:
    data = list()
    columns = ["value", "option", ]
    for option in ["Filter Name", "Description", "Symbol", "Colour", *[f"Hide {rarity} from Level" for rarity in ["Normal", "Magic", "Rare", "Exalted", "Set", "Unique"]], ]:
        data.append([None, option])
    data = pd.DataFrame(data, columns=columns)
    return data

def filter_options_sheet() -> pd.DataFrame:
    data = list()
    columns = ["value", "option", ]
    for option in ["Filter Name", "Description", "Symbol", "Colour", *[f"Hide {rarity} from Level" for rarity in ["Normal", "Magic", "Rare", "Exalted", "Set", "Unique"]], ]:
        data.append([None, option])
    data = pd.DataFrame(data, columns=columns)
    return data

def affix_advanced_options_sheet(slot_map: dict[str,str]) -> pd.DataFrame:
    data = list()
    rule_names = ["rule_group", "rule", ]
    rule_slots = [None, "Slot", ]
    for name, slot in slot_map.items():
        rule_names.append(name)
        rule_slots.append(slot)
    data.append(rule_slots)
    for affix_group in AFFIX_GROUPS[::-1]:
        for option in AFFIX_ADVANCED_OPTIONS:
            data.append([affix_group, option, *[None for _ in slot_map.items()], ])
    for option in RULE_OPTIONS:
        data.append([None, option, *[None for _ in slot_map.items()], ])
    data = pd.DataFrame(data, columns=rule_names)
    return data

def main() -> pd.DataFrame:
    id_dict = json.load(open(filepaths["affix_id"]["game_data"]["processed"].joinpath("affix_id.json"), "r"))
    id_dict = _deconstruct_id_dict(id_dict)
    id_frame = pd.DataFrame.from_records(id_dict)
    details_dict = json.load(open(filepaths["affix_id"]["details"]["processed"].joinpath("affix_details.json"), "r"))
    details_dict = _deconstruct_details_dict(details_dict)
    details_frame = pd.DataFrame.from_records(details_dict)
    affix_frame = id_frame.merge(details_frame, left_on=["title"], right_on=["name"], how="outer", validate="m:m", indicator=True)
    affix_frame = affix_frame.loc[affix_frame.apply(_keep_row, axis=1)].drop(columns=["name", "applies_to"])
    affix_frame["keep"] = affix_frame.groupby(by=["slot", "id"], as_index=False).apply(_match_affix_type, include_groups=False).droplevel(0, axis=0)
    affix_frame = affix_frame.loc[affix_frame["keep"]].drop(columns=["keep"])
    affix_frame["keep"] = affix_frame.groupby(by=["slot", "id"], as_index=False).apply(_match_affix_class, include_groups=False).droplevel(0, axis=0)
    affix_frame = affix_frame.loc[affix_frame["keep"]].drop(columns=["keep"])
    affix_frame["slot"] = pd.Categorical(affix_frame["slot"], SLOT_ORDER, ordered=True)
    affix_frame["group"] = pd.Categorical(affix_frame["group"], GROUP_ORDER, ordered=True)
    affix_frame = affix_frame.sort_values(by=["slot", "group", "position", "title"])
    return affix_frame

if __name__ == "__main__":
    df = main()
    # df.drop(columns=["_merge"]).to_csv(filepaths["affix_id"]["combined"].joinpath("affix.csv"), index=False, encoding="utf-8")
    affix_out_filepath = filepaths["affix_id"]["combined"].joinpath("affix.xlsx")
    with pd.ExcelWriter(affix_out_filepath, engine="openpyxl", mode="w") as xlfile:
        filter_options_sheet().to_excel(xlfile, index=False, sheet_name="Filter Options")
        affix_advanced_options_sheet(BASIC_FILTER_SLOTS).to_excel(xlfile, index=False, sheet_name="Advanced Options")
        for rule_id, slot in BASIC_FILTER_SLOTS.items():
            slot = META_SLOT_SELECTOR.get(slot, [slot, ])
            gdf = df.loc[lambda df: df["slot"].isin(slot)]
            gdf = gdf.groupby(by=["id"], as_index=False).agg({
                **{"slot": lambda sr: ",".join(sr.tolist())}, 
                **{col: "first" for col in gdf.columns if col not in ["slot", "id", ]}
            }).sort_values(by=["position", "group", "title", ])
            gdf.reindex(columns=[*AFFIX_GROUPS, *gdf.columns, ]).to_excel(xlfile, index=False, sheet_name=rule_id)
    format_workbook(affix_out_filepath, freeze_panes=(2, len(AFFIX_GROUPS) + 1), wrap_text=True)
    wb = load_workbook(affix_out_filepath)
    format_sheet(wb["Filter Options"], freeze_panes=(2, 2), wrap_text=True)
    format_sheet(wb["Advanced Options"], freeze_panes=(2, 3), wrap_text=True)
    wb.save(affix_out_filepath)
    wb.close()
    # df.loc[df[["slot", "id"]].duplicated(keep=False)].to_csv(filepaths["affix_id"]["combined"].joinpath("check.csv"), index=False, encoding="utf-8")
