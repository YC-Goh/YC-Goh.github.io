
import pandas as pd
import json
from lxml import etree
from _001_base import *

def parse_rules_to_xml(rules: dict) -> etree.Element:
    XHTMLNS = "http://www.w3.org/2001/XMLSchema-instance"
    XHTML = "{%s}" % XHTMLNS
    NSMAP = {"i": XHTMLNS}
    itemfilter = etree.Element("ItemFilter", nsmap=NSMAP)
    itemfilter_name = etree.SubElement(itemfilter, "name")
    itemfilter_name.text = "Filter"
    itemfilter_icon = etree.SubElement(itemfilter, "filterIcon")
    itemfilter_icon.text = "0"
    itemfilter_colour = etree.SubElement(itemfilter, "filterIconColor")
    itemfilter_colour.text = "0"
    itemfilter_description = etree.SubElement(itemfilter, "description")
    itemfilter_description.text = ""
    itemfilter_gameversion = etree.SubElement(itemfilter, "lastModifiedInVersion")
    itemfilter_gameversion.text = LATEST_GAME_VERSION
    itemfilter_version = etree.SubElement(itemfilter, "lootFilterVersion")
    itemfilter_version.text = LATEST_FILTER_VERSION
    itemfilter_rules = etree.SubElement(itemfilter, "rules")
    rules_rule = etree.SubElement(itemfilter_rules, "Rule")
    rule_type = etree.SubElement(rules_rule, "type")
    rule_type.text = "HIDE"
    rule_isEnabled = etree.SubElement(rules_rule, "isEnabled")
    rule_isEnabled.text = "true"
    rule_Order = etree.SubElement(rules_rule, "Order")
    rule_Order.text = "0"
    for i, (slot, rule) in zip(range(1, 1 + len(rules.keys()), 1), rules.items()):
        rules_rule = etree.SubElement(itemfilter_rules, "Rule")
        rule_type = etree.SubElement(rules_rule, "type")
        rule_type.text = "SHOW"
        rule_isEnabled = etree.SubElement(rules_rule, "isEnabled")
        rule_isEnabled.text = "true"
        rule_Order = etree.SubElement(rules_rule, "Order")
        rule_Order.text = f"{i:.0f}"
        rule_conditions = etree.SubElement(rules_rule, "conditions")
        conditions_condition = etree.SubElement(rule_conditions, "Condition")
        conditions_condition.set(f"{XHTML}type", "SubTypeCondition")
        condition_type = etree.SubElement(conditions_condition, "type")
        condition_subtype = etree.SubElement(conditions_condition, "subTypes")
        for equipmenttype in SLOT_TO_TYPE_MAP[slot]:
            type_equipmenttype = etree.SubElement(condition_type, "EquipmentType")
            type_equipmenttype.text = equipmenttype
        for j, (affix_group, group_rule) in enumerate(rule.items()):
            affix_ids = group_rule["affix_ids"]
            min_affix = group_rule["Minimum Number of Affixes"]
            min_tier = group_rule["Minimum Tier"]
            if not (min_tier == min_tier and min_tier):
                min_tier = 1
            min_total_tier = group_rule["Minimum Total Tier"]
            if not (min_total_tier == min_total_tier and min_total_tier):
                min_total_tier = 1
            conditions_condition = etree.SubElement(rule_conditions, "Condition")
            conditions_condition.set(f"{XHTML}type", "AffixCondition")
            condition_affixes = etree.SubElement(conditions_condition, "affixes")
            for affix_id in affix_ids:
                affixes_affix = etree.SubElement(condition_affixes, "int")
                affixes_affix.text = f"{affix_id:.0f}"
            condition_advanced = etree.SubElement(conditions_condition, "advanced")
            condition_advanced.text = "true"
            condition_affix_count = etree.SubElement(conditions_condition, "minOnTheSameItem")
            condition_affix_count.text = f"{min_affix:.0f}"
            condition_comparison = etree.SubElement(conditions_condition, "comparsion")
            condition_comparison.text = "ANY" if min_tier <= 1 else "MORE_OR_EQUAL"
            condition_comparsion_value = etree.SubElement(conditions_condition, "comparsionValue")
            condition_comparsion_value.text = f"{min_tier:.0f}"
            condition_combined_comparision = etree.SubElement(conditions_condition, "combinedComparsion")
            condition_combined_comparision.text = "ANY" if min_total_tier <= 1 else "MORE_OR_EQUAL"
            condition_combined_comparision_value = etree.SubElement(conditions_condition, "combinedComparsionValue")
            condition_combined_comparision_value.text = f"{min_total_tier:.0f}"
        rule_color = etree.SubElement(rules_rule, "color")
        rule_color.text = "0"
        rule_emphasized = etree.SubElement(rules_rule, "emphasized")
        rule_emphasized.text = "false"
        rule_nameOverride = etree.SubElement(rules_rule, "nameOverride")
        # rule_nameOverride.text = ""
        rule_SoundId = etree.SubElement(rules_rule, "SoundId")
        rule_SoundId.text = "0"
        rule_BeamId = etree.SubElement(rules_rule, "BeamId")
        rule_BeamId.text = "0"
    return itemfilter

def parse_affixes_to_dict(input_folder: Path) -> dict:
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

def main(input_folder: Path) -> Tuple[dict, etree.Element]:
    affixes = parse_affixes_to_dict(input_folder)
    # print(json.dumps(affixes, indent=2))
    itemfilter = parse_rules_to_xml(affixes)
    # print(etree.tostring(itemfilter, pretty_print=True).decode())
    return affixes, itemfilter

if __name__ == "__main__":
    rules, itemfilter = main(filepaths["filter_maker"]["input"])
    with open(filepaths["filter_maker"]["output"].joinpath("filter.xml"), "wt") as file:
        file.write(etree.tostring(itemfilter, pretty_print=True).decode())
