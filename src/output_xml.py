import xml.etree.ElementTree as ET
import inputData

def getTestCaseName(filename):
    test_case_name = filename.split('/')[-1].split('.')[0]
    return test_case_name

def indent(elem, level=0):
    i = "\n" + level*"    "
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = i + "    "
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
    for elem in elem:
        indent(elem, level+1)
    if not elem.tail or not elem.tail.strip():
        elem.tail = i
    else:
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = i

def outputSolutionXML(tsn, filename="default.xml"):
    """
    Outputs TSN solution to XML file called "solution.xml", located in same directory.
    :param TSN:
    :return: solution.xml
    """
    root = ET.Element("solution")

    test_case = getTestCaseName(filename)
    root.set('tc_name', test_case)

    for s in tsn.streams:
        stream = ET.SubElement(root, "stream")
        stream.set('id', s.id)
        for r in range(len(s.solution_routes)):
            route = ET.SubElement(stream, "route")
            for i in range(len(s.solution_routes[r])-1):

                link_element = ET.SubElement(route, "link")
                src_device = s.solution_routes[r][i]
                dest_device = s.solution_routes[r][i + 1]

                for link in tsn.links:
                    if (link.src == src_device) and (link.dest == dest_device):
                        link_element.set('src', str(link.src.name))
                        link_element.set('dest', str(link.dest.name))

    indent(root)
    tree = ET.ElementTree(root)

    with open(test_case+'_solution.xml', "wb") as files:
        tree.write(files, encoding="utf-8")
