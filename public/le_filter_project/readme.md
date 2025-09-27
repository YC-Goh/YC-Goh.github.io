#   Last Epoch Filter Maker

##  Versions

|   Version |   Date    |   Short Description   |
|   ----    |   ----    |   ----    |
|   1.0.0   |   2025-09 |   First release. Program only, no user interface. Covers filtering uniques / sets (no filtering on mod range yet) and filtering items by affixes (no filtering on item sub-type yet). |

##  Introduction

This is a personal project made because the in-game loot filter maker, while useful, lacked a lot of usability features like saving affix sets and copying rule conditions for re-use. If this loot filter maker works the way I need it to, I think there is a good chance that there are other players that this is useful for, hence this release.

To be sure, this is not the first player-made filter maker. However, the LE Tools filter maker is just a browser version of the in-game thing and other popular websites either do not really have one or they only host filter making guides or filters for popular builds. This is not what I want, as I need a way to customise my own filter for my own strategy.

In short, use this to make your own filter if you need a specific strategy different enough from build guide filters or is very troublesome to make and maintain using the in-game interface.

##  How to use

### Set-Up

Create a folder (any name), and in the folder keep filter_maker_x86.exe, and a folder called filter_maker. In filter_maker, create 3 sub-folders input, output, and raw. Keep an original unedited version of filter.xlsx in raw for safekeeping at all times, since there is no protection implemented on this file and you can easily delete information needed for the filter to compile correctly.

Visually, the folder should look like this

[Folder]
  |-  filter_maker_x86.exe
  |-  filter_maker
        |-  input
              |-  [your completed XLSX filter files]
        |-  output
              |-  [compiled filter files]
        |-  raw
              |-  filter.xlsx

### Create Filter

Make a copy of filter.xlsx from raw to input. Rename it to anything you like as long as it starts with "filter" and maintains the ".xlsx" extension to denote an XML Excel file. Open the file and read the instructions on the first sheet, then edit / fill it out accordingly. 

Hint: 
1.  You can create more sheets and more columns in Advanced Options. There is no limit, as long as the headers in Advanced Options correspond to a sheet.
2.  Start with 1 or 2 rules first and check that the filter compiles properly and the rules do what you expect it to do in-game. Then, fill out the rest of your filter.
3.  Do not delete rows in any sheet. The program looks for quite specific information to align itself, so any missing rows can result in failure to compile.

### Compile Filter

Once you complete your filters, run filter_maker_x86.exe. It will create a pair of JSON and XML files per filter Excel file. If it does not, then some failure happened. Right now the program does not output any logs for checking what went wrong, so your best bet is to redo the filter Excel and try to follow the instructions again.

### Import to Game

The XML files in output are the actual loot filters. For convenience, suggest you open them in Notepad or any other plaintext reader, then Select All, then copy to clipboard (Ctrl + C), then in-game, open the loot filter panel, click the "+", then select the last option "Paste from Clipboard".
