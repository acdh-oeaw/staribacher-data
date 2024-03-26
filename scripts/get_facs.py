#!/usr/bin/env python3
# adjusts the facs urls
# adds ids to the p elements
# removes dataline

from lxml import etree
import os
from acdh_tei_pyutils.tei import TeiReader
import dateparser


def remove_dateline_tag(xml_doc):
    if xml_doc.any_xpath("//tei:dateline/tei:date/text()"):
        datetext = xml_doc.any_xpath("//tei:dateline/tei:date/text()")[0]
        datetext_full = "".join(datetext.getparent().itertext())
        date = datetext.getparent()
        div = date.getparent().getparent()
        div.remove(date.getparent())
        date_index = date.getparent().index(date)
        if dateparser.parse(datetext) is None:
            p_elem = etree.Element("p")
            p_elem.attrib["%sspace" % xml_namespace] = "preserve"
            p_elem.text = datetext_full
            div.insert(date_index, p_elem)


def change_facs_url(root):
    url = "https://iiif.acdh-dev.oeaw.ac.at/iiif/images/staribacher/"
    imgs = root.findall(".//" + tei_namespace + "pb")
    for img in imgs:
        img_str = img.get("facs")
        volume = img_str.split("_")[0]
        jpg = img_str.split(".")[0]
        new_url = url + "Band" + volume + "/" + jpg + ".jp2/full/pct:100/0/default.jpg"
        img.set("facs", new_url)


def create_ids_for_p(xml_doc, root):
    doc_id = xml_doc.any_xpath('//tei:idno[@type="signature"]/text()')[0]
    paras = root.findall(".//" + tei_namespace + "p")
    i = 0
    for para in paras:
        i += 1
        para_id = doc_id + "_" + "{:02}".format(i)
        para.set(xml_namespace + "id", para_id)


def get_file_input(xml_file_path):
    xml_doc = TeiReader(xml_file_path)
    root = xml_doc.tree.getroot()
    return (xml_doc, root)


folder_path = "../data/editions"
xml_files = [f for f in os.listdir(folder_path) if f.endswith(".xml")]

for xml_file in xml_files:
    xml_file_path = os.path.join(folder_path, xml_file)
    xml_doc, root = get_file_input(xml_file_path)
    tei_namespace = f'{{{xml_doc.ns_tei.get("tei")}}}'
    xml_namespace = f'{{{xml_doc.ns_xml.get("xml")}}}'
    remove_dateline_tag(xml_doc)
    xml_doc.tree_to_file(xml_file_path)  # write to file
    xml_doc, root = get_file_input(xml_file_path)  # load file again with changes
    change_facs_url(root)
    create_ids_for_p(xml_doc, root)
    xml_doc.tree_to_file(xml_file_path)
