
import pandas as pd
import json
from lxml import etree as et
from _001_base import *

XHTMLNS = "http://www.w3.org/2001/XMLSchema-instance"
XHTML = "{%s}" % XHTMLNS
def XHTML_TAG(tag: str):
    return f"{XHTML}{tag}"
NSMAP = {"i": XHTMLNS}

def __float_to_str(val: float) -> str:
    if int(val) == val:
        return f"{val:.0f}"
    else:
        return f"{val:.2f}"

def json_to_etree(element: et.Element, filter_json: dict) -> et.Element:
    for sub_tag, sub_tag_value in filter_json.items():
        if sub_tag == "_attributes":
            for attr, attr_value in sub_tag_value.items():
                element.set(XHTML_TAG(attr), attr_value)
        elif sub_tag == "_values":
            for sub_tag_value in sub_tag_value:
                json_to_etree(element, sub_tag_value)
        else:
            sub_element = et.SubElement(element, sub_tag)
            if sub_tag_value == sub_tag_value and sub_tag_value is not None:
                if isinstance(sub_tag_value, (int,)):
                    sub_element.text = f"{sub_tag_value:.0f}"
                elif isinstance(sub_tag_value, (float,)):
                    sub_element.text = __float_to_str(sub_tag_value)
                elif isinstance(sub_tag_value, (str,)):
                    sub_element.text = sub_tag_value
                elif isinstance(sub_tag_value, (bool,)):
                    sub_element.text = "true" if sub_tag_value else "false"
                elif isinstance(sub_tag_value, (dict,)):
                    json_to_etree(sub_element, sub_tag_value)
                elif isinstance(sub_tag_value, (list,)):
                    for sub_sub_element_json in sub_tag_value:
                        json_to_etree(sub_element, sub_sub_element_json)
    return element

def main(input_file: Path) -> et.Element:
    filter_rules = json.loads(open(input_file, "rt").read())
    itemfilter = et.Element("ItemFilter", nsmap=NSMAP)
    itemfilter = json_to_etree(itemfilter, filter_rules)
    return itemfilter

if __name__ == "__main__":
    itemfilter = main(filepaths["filter_maker"]["output"].joinpath("filter.json"))
    with open(filepaths["filter_maker"]["output"].joinpath("filter.xml"), "wt") as file:
        file.write(et.tostring(itemfilter, pretty_print=True, encoding='utf-8').decode())