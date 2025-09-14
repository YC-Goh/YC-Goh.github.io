Folder structure description format:
1.  Folders: folder_name [source]
    1.  Note: source is only listed for folders directly containing data files
2.  Files: file_name.ext [schema]
    1.  Schema for JSON, HTML, XML files:
        1.  Type 1: {level_0_0 (type): value, level_0_1 (type): value, ...}
        2.  Type 2: [{level_0_0 (type): value, level_0_1 (type): value, ...}]
            -   [{...}] implies a list of {...}
        3.  value takes either Type 1 or Type 2 for nested JSON, or a single value or [list of values] for final values.
    2.  Schema for CSV files: col1 (type), col2 (type), col3 (type), ..., colN (type)
    3.  Note: [file_name1-file_name2] and [file_name1/file_name2/...] indicate range of files sharing same schema. 
    4.  Note: some schemas may not yet be filled out
    5.  Note: possible types are str, int, dbl, bool

Folder structure:
-   affix_id
    -   combined [data pipeline output]
    -   details
        -   processed [data pipeline output]
        -   raw [https://www.lastepochtools.com/db/]
            -   [prefix/suffix].html
    -   game_data
        -   processed [manual processing output]
            -   affix_id.csv [affix_id (int), affix_class (str), affix_group (str), affix_name (str)]
        -   raw [in-game data scraping]
            -   affix_id.xml
    -   idol_tiers
        -   processed [data pipeline output]
            -   [01-05].csv [Affix Type (str), Name (str), Reroll % (str), Tier1 (str), Tier2 (str), Tier3 (str), Tier4 (str), Tier5 (str), Tier6 (str), Tier7 (str), Source File (str)]
            -   [01-05].json
            -   data.csv [Affix Type (str), Name (str), Reroll % (str), Tier1 (str), Tier2 (str), Tier3 (str), Tier4 (str), Tier5 (str), Tier6 (str), Tier7 (str), Source File (str)]
            -   data.json
        -   raw [https://lastepoch.tunklab.com/affixes]
            -   [01-05].html
    -   item_tiers
        -   processed [data pipeline output]
            -   [01-05].csv [Affix Type (str), Lvl (int), Name (str), Reroll % (str), Tier1 (str), Tier2 (str), Tier3 (str), Tier4 (str), Tier5 (str), Tier6 (str), Tier7 (str), Tier8 (str), Source File (str)]
            -   [01-05].json
            -   data.csv [Affix Type (str), Lvl (int), Name (str), Reroll % (str), Tier1 (str), Tier2 (str), Tier3 (str), Tier4 (str), Tier5 (str), Tier6 (str), Tier7 (str), Tier8 (str), Source File (str)]
            -   data.json
        -   raw [https://lastepoch.tunklab.com/affixes]
            -   [01-05].html
-   condition_list
    -   processed [data pipeline output]
    -   raw [in-game data scraping]
        -   condition_list.xml
-   item_id
    -   combined [data pipeline output]
    -   details
        -   processed [data pipeline output]
        -   raw [in-game data scraping]
            -   [1h_axe/1h_dagger/1h_mace/1h_sceptre/1h_sword/1h_wand/2h_axe/2h_bow/2h_mace/2h_spear/2h_staff/2h_sword/amulet/armour/belt/boots/catalyst/gloves/helmet/quiver/relic/ring/shield/type].html
    -   game_data
        -   processed [manual processing output]
        -   raw [in-game data scraping]
-   unique_id
    -   combined [data pipeline output]
    -   details
        -   processed [data pipeline output]
            -   all.json
        -   raw [https://www.lastepochtools.com/db/]
            -   all.html
    -   game_data
        -   processed [data pipeline output]
        -   raw [in-game data scraping]
    -   lp_tiers
        -   processed [data pipeline output]
        -   raw [https://lastepoch.tunklab.com/uniques]
            -   [01-05].html
-   _011_affix_tiers_table_parser.py
-   _012_affix_tiers_file_merger.py
-   _013_affix_tiers_batch_processor.py
-   _021_affix_details_table_parser.py
-   _022_affix_details_json_parser.py
-   _031_unique_details_table_parser.py