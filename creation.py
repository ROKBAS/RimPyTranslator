import xml.dom.minidom as md
import xml.etree.ElementTree as ET


def create_def_xml(def_strings, path):
    root = ET.Element("LanguageData")
    for _id, string in def_strings:
        _string = ET.SubElement(root, _id)
        _string.text = string
    xmlstr = ET.tostring(root).decode()
    newxml = md.parseString(xmlstr)
    with open(path, "wb+") as outfile:
        outfile.write(newxml.toprettyxml(indent="\t", newl="\n", encoding="utf-8"))


def create_keyed_xml(keyed_strings, path):
    root = ET.Element("LanguageData")
    for _id, string in keyed_strings:
        _string = ET.SubElement(root, _id)
        _string.text = string
    xmlstr = ET.tostring(root).decode()
    newxml = md.parseString(xmlstr)
    with open(path, "wb+") as outfile:
        outfile.write(newxml.toprettyxml(indent="\t", newl="\n", encoding="utf-8"))


def create_patch_xml(patch_strings, path):
    root = ET.Element("LanguageData")
    for _id, string in patch_strings:
        _string = ET.SubElement(root, _id)
        _string.text = string
    xmlstr = ET.tostring(root).decode()
    newxml = md.parseString(xmlstr)
    with open(path, "wb+") as outfile:
        outfile.write(newxml.toprettyxml(indent="\t", newl="\n", encoding="utf-8"))


def create_strings_text(string_strings, path):
    with open(path, "w+") as file:
        file.writelines(string_strings)
