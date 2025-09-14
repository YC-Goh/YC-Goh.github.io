
import re
from pathlib import Path

filepaths = dict()
filepaths["project"] = Path(".").absolute()
filepaths = {
    "affix_id": filepaths["project"].joinpath("affix_id"), 
    "item_id": filepaths["project"].joinpath("item_id"), 
    "unique_id": filepaths["project"].joinpath("unique_id"), 
    "condition_list": filepaths["project"].joinpath("condition_list"), 
}
for key in ["affix_id", "item_id", "unique_id"]:
    filepaths[key] = {
        "combined": filepaths[key].joinpath("combined"), 
        "game_data": {
            "processed": filepaths[key].joinpath("game_data", "processed"), 
            "raw": filepaths[key].joinpath("game_data", "raw"), 
        }, 
        "details": {
            "processed": filepaths[key].joinpath("details", "processed"), 
            "raw": filepaths[key].joinpath("details", "raw"), 
        }, 
    }

def strip_ws(text: str) -> str:
    return re.compile(r"\s+").sub(" ", text)
