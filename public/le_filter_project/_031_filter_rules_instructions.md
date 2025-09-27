#   Filter Options

1.  Filter Name: What to call your filter. Defaults to New Filter if blank.
2.  Description: The description box. Can be left blank.
3.  Symbol: The logo. Input should be a number. Mapping of number to the in-game symbol is coming up.
4.  Colour: Logo colour. Input should be a number. Mapping of number to the in-game colour is coming up.
5.  Hide Normal/Magic/Rare/Exalted/Unique/Rare from Level: Hide these rarities after what level. Leave blank to never do this.
    1.  Normal: Suggest halfway through Chapter 1.
    2.  Magic/Rare: Suggest around when you start Empowered Monoliths.
    3.  Exalted/Set/Unique: Suggest do not set unless you know what you are doing.
    4.  Note: This is not the end-of-filter Hide All rule. These are the first rules in the filter and will hide absolutely ALL items of that rarity!

#   Uniques Options

1.  Show LP4 / WW24 or higher: This is the highest bar. You can leave this blank as the filter maker auto-imputes from all lower levels. Effectively, if you do not fill this out, then any unique that you do not mark anywhere is by default hidden. Useful for permanently leaving off any set or unique idol that you don't care about.
2.  Show LP3 / WW18 or higher: Very high bar. Suggest this is only ticked for items that (1) drop very commonly, AND (2) have very low LP level. This is so that for sufficiently low-value uniques, you see only the most interesting drops. Rule of thumb for low LP level is below 30.
3.  Show LP2 / WW12 or higher: High bar. Similar to the LP3 rule, suggest to show for items that drop very commonly AND have moderate LP level. Rule of thumb, from 30 to below 70.
4.  Show LP1 / WW6 or higher: Low bar. Reserve for items that drop sufficiently commonly enough but have high LP level, so that you don't miss anything of interest.
5.  Show LP0 / WW0 or higher: No bar. Use this for items that you see very rarely either because the reroll chance is very high or is a difficult boss's special drop, so that you get another chance to rolling LP using Nemesis.

Note that all legendaries are currently shown by default. There is a way to filter legendaries by number of modifiers and even what modifiers were rolled on it, but that will be a future update.

#   Advanced (Affix) Options

Each column corresponds to one rule in the in-game filter (a rule is a collection of conditions that identify items to hide or show). The column header is the rule ID (NOT the rule name), for which a corresponding sheet with the sheet name being the rule ID must exist. Note that the column header is independent of the slot. Hence, it is possible to have multiple rules for the same item slot (e.g., if looking for items for different builds, or one rule for finding items for crafting while another rule is for finding shards)

1.  Slot: This tells the filter maker what equipment slot this rule is for. This corresponds to the Item Type condition. Note that the filter maker will not check that this corresponds to the actual affix list in the corresponding affix sheet.
2.  Affix Group 1/2/3/4/5/6: Up to 6 affix groups to customise what this rule looks for. These affixes are for Magic / Rare / Exalted / Reforged Set / Idol items. Advanced options are presented in this sheet while affixes are in the respective affix sheets.
    1.  Suboptions: (1) Use Group: Use this group or not? Just enter "1" if so; (2) Minimum Number of Affixes: At least How many affixes from this group?; (3) Minimum Tier: At least what tier affixes?; (4) Minimum Total Tier: At least what total tier across all affixes from this group that spawns?
    2.  Note that the filter maker does not enforce that any affix must be selected if Use Group is indicated, and neither does it try to guess Use Group from whether any affixes in that group are selected.
    3.  For the respective linked affix sheet of the rule, indicate the affixes to include in that group by just entering "1".
3.  Rule Description: Custom name for this rule. Can leave blank if not necessary
4.  Recolour: Indicate the colour ID for this rule to recolour shown drops. Defaults to "0" (default colour of that rarity).
5.  Sound: Indicate the sound ID for this rule. Defaults to "0" (default sound of that rarity).
6.  Beam Colour: Indicate the colour ID of the item beam for this rule. Defaults to "0" (default colour of that rarity).
7.  Acolyte/Primalist/Mage/Rogue/Sentinel: Indicate if this Rule should only show items usable by the class(es). Just indicate using "1". If all or none are selected, defaults to "Any" class.

To create more item affix rules, just create a new column and give it a name, and then find the appropriate item slot sheet and copy it and rename it to the same rule name. Take note of the following meta slots:
1.  All One-Handed Weapons
2.  All Two-Handed Weapons
3.  All Weapons
4.  All Off-Hand: Off-Hands are Catalysts, Shields, and Quivers
5.  All Armour: Armours are Helmets, Body Armours, Boots, Gloves, and Belts
6.  All Jewellery: Jewellery are Amulets, Rings, and Relics
7.  All Equipment: Equipments are Off-Hands, Armours, and Jewellery
8.  All Generic Idols: These are the size 1 and 2 (small) idols
9.  All Class-Specific Idols: THese are the size 3 and 4 (large) idols
10. All Idols

#   Common Patterns for Advanced Options

1.  Show items with N of X affixes using only affix group 1 with minimum affixes N.
2.  Show items with N affixes, each from its own pool using affix groups 1/2/.../N each with minimum affixes 1.
3.  Show items with N affixes in an expanding set using affix groups 1/2/.../N, where group 1 is the smallest set and minimum affix 1, up to group N being largest with minimum affixes N.
