#!/usr/bin/env python3
# Run just once from the top directory to add a xml:id attrib to  the TEI
# files in data/editions. It uses the file name without extension
import os
from acdh_tei_pyutils.tei import TeiReader, ET

xml_path = "./data/editions"
xml_files = [f for f in os.listdir(xml_path) if
             f.startswith("staribacher__") and f.endswith(".xml")]

xml_prev = ""
for xml_file in xml_files:
    xml_filepath = f"{xml_path}/{xml_file}"
    xml_doc = TeiReader(xml_filepath)
    tei_ns = xml_doc.ns_tei
    xml_doc_root = xml_doc.tree.getroot()
    xml_doc_root.attrib[f'{{{xml_doc.ns_xml.get("xml")}}}id'] = os.path.splitext(xml_file)[0]
    if xml_prev:
        xml_doc_root.attrib['prev'] = xml_prev
        xml_prev_filepath = f"{xml_path}/{xml_prev}"
        xml_prev = TeiReader(xml_prev_filepath)
        xml_prev_root = xml_prev.tree.getroot()
        xml_prev_root.attrib['next'] = xml_file
        with open(xml_prev_filepath, "wb") as f:
            f.write(ET.tostring(xml_prev_root, pretty_print=True))
    xml_prev = xml_file

    with open(xml_filepath, "wb") as f:
        f.write(ET.tostring(xml_doc_root, pretty_print=True))
