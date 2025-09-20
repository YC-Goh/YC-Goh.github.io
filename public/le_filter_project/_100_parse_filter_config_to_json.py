
import pandas as pd
import json
from _001_base import *

HIDE_ALL = {
    "Rule": {
        "type": "HIDE", 
        "conditions": None, 
        "color": 0, 
        "isEnabled": "true", 
        "emphasized": "false", 
        "nameOverride": None, 
        "SoundId": 0, 
        "BeamId": 0, 
    }
}

def parse_filter_options(filter_options: pd.DataFrame) -> dict:
    filter_options = filter_options.set_index(keys=["option"], append=False)["value"].copy(deep=True)
    filter_name = replace_if_na(filter_options["Filter Name"], "New Filter")
    filter_description = replace_if_na(filter_options["Description"], None)
    filter_symbol = replace_if_na(filter_options["Symbol"], 0)
    filter_colour = replace_if_na(filter_options["Colour"], 0)
    hide_normal_from = replace_if_na(filter_options["Hide Normal from Level"], 101)
    hide_magic_from = replace_if_na(filter_options["Hide Magic from Level"], 101)
    hide_rare_from = replace_if_na(filter_options["Hide Rare from Level"], 101)
    hide_exalted_from = replace_if_na(filter_options["Hide Exalted from Level"], 101)
    hide_unique_from = replace_if_na(filter_options["Hide Unique from Level"], 101)
    hide_legendary_from = 101
    hide_set_from = replace_if_na(filter_options["Hide Set from Level"], 101)
    filter_options = {
        "name": filter_name, 
        "description": filter_description, 
        "lastModifiedInVersion": LATEST_GAME_VERSION, 
        "lootFilterVersion": LATEST_FILTER_VERSION, 
        "filterIcon": filter_symbol, 
        "filterIconColor": filter_colour, 
    }
    hide_rules = list()
    def _hide_rule(rarity: str, level_from: int) -> dict:
        return {
            "Rule": {
                "type": "HIDE", 
                "conditions": [
                    {
                        "Condition": {
                            "attributes": {"type": "RarityCondition"}, 
                            "rarity": rarity, 
                            "minLegendaryPotential": {"attributes": {"nil": "true"}}, 
                            "maxLegendaryPotential": {"attributes": {"nil": "true"}}, 
                            "minWeaversWill": {"attributes": {"nil": "true"}}, 
                            "maxWeaversWill": {"attributes": {"nil": "true"}}, 
                        }
                    }, 
                    {
                        "Condition": {
                            "attributes": {"type": "CharacterLevelCondition"}, 
                            "minimumLvl": level_from, 
                            "maximumLvl": 100
                        }
                    }
                ], 
                "type": "HIDE", 
                "isEnabled": "true", 
                "nameOverride": None, 
                "color": 0, 
                "SoundId": 0, 
                "BeamId": 0, 
            }
        }
    for rarity, level in zip(RARITY_ORDER, [hide_normal_from, hide_magic_from, hide_rare_from, hide_exalted_from, hide_unique_from, hide_legendary_from, hide_set_from]):
        if level <= 100:
            hide_rules.append(_hide_rule(rarity, level))
    filter_options['rules'] = hide_rules
    return filter_options

def parse_affix_rule_options(condition_options: pd.Series, affix_options: pd.DataFrame) -> dict:
    rule = {"Rule": {"conditions": list()}}
    conditions = condition_options.copy(deep=True)
    for condition_group, options in conditions.groupby(by="rule_group", group_keys=False, dropna=False):
        options = options.reset_index(level="rule_group", drop=True)
        if condition_group == condition_group and condition_group:
            use_group = options["Use Group"]
            if use_group == use_group:
                affixes = affix_options.loc[affix_options[condition_group].notna(), "id"].tolist()
                affixes = [{"int": f"{affix_id:.0f}"} if isinstance(affix_id, (int, float, )) else affix_id for affix_id in affixes]
                min_n_affix = replace_if_na(options["Minimum Number of Affixes"], 1)
                min_tier = replace_if_na(options["Minimum Tier"], 1)
                min_total_tier = replace_if_na(options["Minimum Total Tier"], 1)
                affix_condition = {
                    "Condition": {
                        "attributes": {"type": "AffixCondition"}, 
                        "affixes": affixes, 
                        "minOnTheSameItem": min_n_affix, 
                        "comparsion": "ANY" if min_tier <= 1 else "MORE_OR_EQUAL", 
                        "comparsionValue": min_tier, 
                        "combinedComparsion": "ANY" if min_total_tier <= min_n_affix else "MORE_OR_EQUAL", 
                        "combinedComparsionValue": min_total_tier, 
                    }
                }
                rule["Rule"]["conditions"].append(affix_condition)
        else:
            slot = options["Slot"]
            description = replace_if_na(options["Rule Description"], None)
            cat_colour = replace_if_na(options["Recolour"], 0)
            cat_sound = replace_if_na(options["Sound"], 0)
            cat_beam = replace_if_na(options["Beam Colour"], 0)
            ind_acolyte = options.notna()["Acolyte"]
            ind_primalist = options.notna()["Primalist"]
            ind_mage = options.notna()["Mage"]
            ind_rogue = options.notna()["Rogue"]
            ind_sentinel = options.notna()["Sentinel"]
            ind_classes = [ind_acolyte, ind_primalist, ind_mage, ind_rogue, ind_sentinel]
            str_classes = ["Acolyte", "Primalist", "Mage", "Rogue", "Sentinel"]
            cat_class = "None"
            if any(ind_classes):
                if not all(ind_classes):
                    cat_class = " ".join([cl for cl, incl in zip(str_classes, ind_classes) if incl])
            item_type_condition = {
                "Condition": {
                    "attributes": {"type": "SubTypeCondition"}, 
                    "type": [{"EquipmentType": item_type} for item_type in SLOT_TO_TYPE_MAP[slot]], 
                }
            }
            class_condition = {
                "Condition": {
                    "attributes": {"type": "ClassCondition"}, 
                    "req": cat_class, 
                }
            }
            rule_options = {
                "type": "SHOW", 
                "isEnabled": "true", 
                "nameOverride": description, 
                "color": cat_colour, 
                "SoundId": cat_sound, 
                "BeamId": cat_beam, 
            }
            rule["Rule"]["conditions"].append(item_type_condition)
            if cat_class != "None":
                rule["Rule"]["conditions"].append(class_condition)
            rule["Rule"] = {**rule["Rule"], **rule_options}
    return rule

def parse_affixes_to_dict(input_folder: Path) -> dict:
    sheets = pd.read_excel(input_folder.joinpath("affix.xlsx"), sheet_name=None)
    filter_options = parse_filter_options(sheets["Filter Options"])
    advanced_options = sheets["Advanced Options"].set_index(keys=["rule_group", "rule"], append=False)
    advanced_options = advanced_options.loc[:, lambda df: df.xs(("Use Group",), 0, ("rule",)).notna().any(axis=0)]
    rules = list()
    for rule_id in advanced_options.columns[::-1]:
        rules.append(parse_affix_rule_options(advanced_options[rule_id], sheets[rule_id]))
    filter_options["rules"] = [HIDE_ALL, *rules, *filter_options["rules"]]
    return filter_options

def main(input_folder: Path) -> dict:
    affixes = parse_affixes_to_dict(input_folder)
    return affixes

if __name__ == "__main__":
    rules = main(filepaths["filter_maker"]["input"])
    with open(filepaths["filter_maker"]["output"].joinpath("filter.json"), "wt") as file:
        file.write(json.dumps(rules, indent=2))
