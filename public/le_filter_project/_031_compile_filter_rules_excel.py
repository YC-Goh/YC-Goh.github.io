
import pandas as pd
import json
from _001_base import *

AFFIX_GROUPS = [f"affix_group_{n:.0f}" for n in range(6, 0, -1)]
AFFIX_ADVANCED_OPTIONS = ["Use Group", "Minimum Number of Affixes", "Minimum Tier", "Minimum Total Tier", ]

UNIQUE_RARITY_GROUPS = [
    "show_lp4_ww24_or_higher", 
    "show_lp3_ww18_or_higher", 
    "show_lp2_ww12_or_higher", 
    "show_lp1_ww06_or_higher", 
    "show_lp0_ww00_or_higher", 
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
    for i in range(1, 2, 1)
}

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

if __name__ == "__main__":
    affix_frame = pd.read_csv(filepaths["affix_id"]["combined"].joinpath("affix.csv"), low_memory=False, encoding="utf-8")
    unique_frame = pd.read_csv(filepaths["unique_id"]["combined"].joinpath("unique.csv"), low_memory=False, encoding="utf-8")
    instruction_sheet = filepaths["project"].joinpath("_031_filter_rules_instructions.md")
    affix_out_filepath = filepaths["filter_maker"]["raw"].joinpath("filter.xlsx")
    instruction_sheet = parse_markdown_to_structured_data(instruction_sheet)
    create_excel_from_structured_data(instruction_sheet, "Instructions", affix_out_filepath)
    with pd.ExcelWriter(affix_out_filepath, engine="openpyxl", mode="a", if_sheet_exists="replace") as xlfile:
        filter_options_sheet().to_excel(xlfile, index=False, sheet_name="Filter Options")
        unique_frame.reindex(columns=[*UNIQUE_RARITY_GROUPS, *unique_frame.columns, ]).to_excel(xlfile, index=False, sheet_name="Uniques")
        affix_advanced_options_sheet(BASIC_FILTER_SLOTS).to_excel(xlfile, index=False, sheet_name="Advanced Options")
        for rule_id, slot in BASIC_FILTER_SLOTS.items():
            slot = META_SLOT_SELECTOR.get(slot, [slot, ])
            gdf = affix_frame.loc[lambda df: df["slot"].isin(slot)]
            gdf = gdf.groupby(by=["id"], as_index=False).agg({
                **{"slot": lambda sr: ",".join(sr.tolist())}, 
                **{col: "first" for col in gdf.columns if col not in ["slot", "id", ]}
            }).sort_values(by=["position", "group", "title", ])
            gdf.reindex(columns=[*AFFIX_GROUPS, *gdf.columns, ]).to_excel(xlfile, index=False, sheet_name=rule_id)
    format_workbook(affix_out_filepath, freeze_panes=(2, len(AFFIX_GROUPS) + 1), wrap_text=True)
    wb = load_workbook(affix_out_filepath)
    format_sheet(wb["Instructions"], freeze_panes=(1, 1), wrap_text=True)
    format_sheet(wb["Filter Options"], freeze_panes=(2, 2), wrap_text=True)
    format_sheet(wb["Uniques"], freeze_panes=(2, len(UNIQUE_RARITY_GROUPS) + 1), wrap_text=True)
    format_sheet(wb["Advanced Options"], freeze_panes=(2, 3), wrap_text=True)
    wb.save(affix_out_filepath)
    wb.close()
