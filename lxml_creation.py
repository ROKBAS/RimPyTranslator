import xml.etree.ElementTree as ET


def create_def_xml(def_strings, path):
    root = ET.Element("LanguageData")
    for _id, string in def_strings:
        _string = ET.SubElement(root, _id)
        _string.text = string
    ET.ElementTree(root).write(path, encoding="utf-8", xml_declaration=True, short_empty_elements=False)


def create_keyed_xml(keyed_strings, path):
    root = ET.Element("LanguageData")
    for _id, string in keyed_strings:
        _string = ET.SubElement(root, _id)
        _string.text = string
    ET.ElementTree(root).write(path, encoding="utf-8", xml_declaration=True, short_empty_elements=False)
