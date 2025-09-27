
import json
from lxml import etree as et
from _001_base import *
from _100_parse_filter_config_to_json import main as parse_config_to_json
from _101_parse_filter_json_to_xml import main as parse_json_to_xml

def main():
    filter_files: list[Path] = list(filepaths["filter_maker"]["input"].glob("filter*.xlsx"))
    for filter_file in filter_files:
        filename = filter_file.name.strip().lower().removesuffix(".xlsx")
        rules = parse_config_to_json(filter_file)
        with open(filepaths["filter_maker"]["output"].joinpath(f"{filename}.json"), "wt") as file:
            file.write(json.dumps(rules, indent=2))
        itemfilter = parse_json_to_xml(filepaths["filter_maker"]["output"].joinpath(f"{filename}.json"))
        with open(filepaths["filter_maker"]["output"].joinpath(f"{filename}.xml"), "wt") as file:
            file.write(et.tostring(itemfilter, pretty_print=True, encoding='utf-8').decode())
    return filter_files

if __name__ == "__main__":
    files = main()
