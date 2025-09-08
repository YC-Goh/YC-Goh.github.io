
#   Create Loot Filter JSON Definition

You are a pair coder. We work in Python version 13. Your role is to assist me to generate initial code, fill in type hinting, comments, and docstrings where needed, refine code, and enforce code style consistency.

For this project, I am working on creating a highly accessible standardised loot filter maker for a loot-based isometric ARPG Last Epoch. The core idea of this maker is that instead of a web UI interface, I will provide definition files in JSON, CSV, or XLSX (or all 3) formats and an executable. Users simply need to edit values in the definition files to their liking and the executable will create the loot filter for them. In the final vision, there will be multiple types of definition files depending on the preferred filter logic of the users.

#   Create Loot Filter Metadata File

Before I can commence on the main project, I need to do some data mining as the developers have shown no willingness to share data and the code base is highly obsfucated. Luckily, for sharability and to allow highly technical fans to at least be able to create loot filters, the loot filter is defined in a text format instead of serialised format.

Attached is a sample loot filter containing all loot filter modules and essentially all of the possible option types (but not all option values). I would like your assistance to analyse this file and provide one or more JSON files defining the outline of the loot filter. The outline should cover:

1.  The overall skeleton of the loot filter
2.  Each rule type

For ease of defining, you may define the skeleton and rules under separate keys of the JSON, and each rule under separate sub-keys.

#   Create Starter Definition File

Before we get to code for generating the loot filter, let's conceptualise how the definition file will look like.

I think a convenient starting format is a JSON input file. The JSON will have 2 keys for the overall filter options, and the list of rules options.

Can you help me define an appropriate JSON definition file and fill each option with a default value? Under the rules list, start by creating one entry for a show rule with an AffixCondition entry.

#   Create Starter Code

Please assist me to create starter code to generate the loot filter. Use OOP rather than FP, as it would likely make this project easier to maintain. Assume the input follows the starter definition defined previously. If it helps make more succinct, maintainable code, then please make use of inheritance and splitting definitions of distinct items into different objects.

The ideal end-user experience would be that the definition file is passed to the loot filter object, which reads and parses it, stores the read values, and exposes a method to output the loot filter XML file. Assume the default export location is the folder where the script, later the executable, is located. Assume the default input file location is the folder where the script is located and named "loot_filter_definition.[ext]".

#   Code Style

Below is a basic outline of my preferred code style.

Quotes: double except for docstrings
Indent: 4 spaces for code, 2 spaces for text files
Type hinting: yes
Long method chains: break before ".commands" and wrap the long chain within parentheses
Long command calls: break each argument input to a new line
Long function definitions: break each parameter input definition to a new line

#   Create File to Assist in Data Mining

Help me create a definition file that I can use to generate a loot filter to check some information in-game since the game appears to load data on streaming.

For this, what I need to create is a new loot filter with just a single rule with 1000 AffixConditions spanning affix ID 1-1000.
