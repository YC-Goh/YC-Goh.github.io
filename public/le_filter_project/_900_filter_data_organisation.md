Folder structure description format:
1.  Folders: folder_name [source]
    1.  Note: source is only listed for folders directly containing data files
2.  Files: file_name.ext [schema]
    1.  Schema for JSON, HTML, XML files:
        1.  Type 1: {level_0_0 (type): value, level_0_1 (type): value, ...}
        2.  Type 2: [{level_0_0 (type): value, level_0_1 (type): value, ...}]
            -   [{...}] implies a list of {...} sharing similar schema
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
            -   affix_details.json
        -   raw [https://www.lastepochtools.com/db/]
    -   game_data
        -   processed [manual processing output]
            -   affix_id.json {id (str): {title (str): value, label (str): value}}
        -   raw [https://www.lastepochtools.com/db/]
-   condition_list
    -   processed [data pipeline output]
    -   raw [in-game data scraping]
-   item_id
    -   combined [data pipeline output]
    -   details
        -   processed [data pipeline output]
        -   raw [in-game data scraping]
    -   game_data
        -   processed [manual processing output]
        -   raw [https://www.lastepochtools.com/db/]
-   unique_id
    -   combined [data pipeline output]
    -   details
        -   processed [data pipeline output]
        -   raw [https://www.lastepochtools.com/db/]
    -   game_data
        -   processed [data pipeline output]
        -   raw [https://www.lastepochtools.com/db/]
    -   lp_tiers
        -   processed [data pipeline output]
        -   raw [https://www.lastepochtools.com/db/]