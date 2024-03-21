#adjusts the facs urls and adds ids to the p elements

from lxml import etree
import os
from acdh_tei_pyutils.tei import TeiReader

folder_path = './data/editions'
url = 'https://iiif.acdh-dev.oeaw.ac.at/iiif/images/staribacher/'
namespace='{http://www.tei-c.org/ns/1.0}'
xml_files = [f for f in os.listdir(folder_path) if f.endswith('.xml')]

for xml_file in xml_files:
    xml_file_path = os.path.join(folder_path, xml_file)
    xml_doc = TeiReader(xml_file_path)
    root = xml_doc.tree.getroot()   
    
    #change facs url
    imgs = root.findall('.//'+namespace+'pb')
    
    for img in imgs:
        img_str = img.get('facs')
        volume = img_str.split('_')[0]
        jpg = img_str.split('.')[0]
        new_url = url+'Band'+volume+'/'+jpg+'.jp2/full/pct:100/0/default.jpg'
        img.set('facs', new_url)

    #create IDs for p elements
    doc_id = xml_doc.any_xpath('//tei:idno[@type="signature"]/text()')[0]
    paras = root.findall('.//'+namespace+'p')
    
    i = 0
    for para in paras:
        i += 1
        para_id = doc_id + '_' + "{:02}".format(i)
        para.set('id', para_id)
    
    #write to file
    xml_doc.tree_to_file(xml_file_path)