#!/usr/bin/env python3
#moves the back element to a div type back element in the body element

import os
from acdh_tei_pyutils.tei import TeiReader
from lxml import etree

folder_path = "../data/editions"
xml_files = [f for f in os.listdir(folder_path) if f.endswith(".xml")]

def get_file_input(xml_file_path):
    xml_doc = TeiReader(xml_file_path)
    root = xml_doc.tree.getroot()
    return (xml_doc, root)

def move_back_element(xml_doc, root):
    body_elem = root.find(".//" + tei_namespace + "body")

    div_elem = etree.Element("div") #create new div element
    div_elem.attrib["type"] = "back"
    
    back_elem = root.find(".//" + tei_namespace + "back")
    if back_elem is not None:
        for child in back_elem:
            div_elem.append(child)
        back_elem.getparent().remove(back_elem)

    body_elem.insert(2, div_elem)
    
for xml_file in xml_files:
    xml_file_path = os.path.join(folder_path, xml_file)
    xml_doc, root = get_file_input(xml_file_path)
    tei_namespace = f'{{{xml_doc.ns_tei.get("tei")}}}'
    move_back_element(xml_doc, root)
    xml_doc.tree_to_file(xml_file_path)