"""
Usage:
Parse single xml file:
x = CtsXmlParser.XmlParser()
x.translate(XML_LOOP1)
x.get_data()
Parse multiple xml file:
x = CtsXmlParser.XmlParser()
x.multi_translate([XML_LOOP1,XML_LOOP2,XML_LOOP3])
x.get_data
"""
from xml.dom import minidom
import ParserBase


def xml_generator(xml_root):
    for node in xml_root.getElementsByTagName("Test"):
        result = node.getAttribute("result")
        pkg,mtd = _getNodeClass(node)
        log = node.getElementsByTagName("FailedScene")[0].getAttribute("message") \
                    if result == "fail" else ""
        yield pkg,mtd,result,log

def _getNodeClass(node):
    rt = []
    while True:
        #node = node.parentNode
        rt.insert(0,node.getAttribute("name"))
        node = node.parentNode
        if node.nodeName =="TestPackage":
            package = node.getAttribute("appPackageName")
            break
    return package,".".join(rt)

class XmlParser(ParserBase.Parser):
    def __init__(self):
        ParserBase.Parser.__init__(self)
        self.xml = None
        self.generator = xml_generator
    def __read(self):
        """Read source file"""
        xml_root = minidom.parse(self.xml).documentElement
        self.result_name = xml_root.getAttribute("testPlan")
        print "Reading file ... %s"%self.xml
        return self.generator(xml_root)
    def translate(self,xml_file):
        """Translate to the format like: {pkg1:{result{class.method:log)}"""
        self.data = {}
        self.xml = xml_file
        for pkg,mtd,result,log in self.__read():
            if pkg in self.data:
                if result in self.data[pkg]:
                    self.data[pkg][result][mtd] = log
                else:
                    self.data[pkg][result] = {mtd:log}
            else:
                self.data[pkg] = {result:{mtd:log}}
    def multi_translate(self,*xmls):
        """Some cts xml result have 3 loops. 
        This method is to merge and translate 3 loops' result to one.
        The xml_files arg should have sequence like: [loop1,loop2,loop3,...]
        """
        for xml in xmls:
            self.translate(xml)
        #self.translate(xml_files[0])
        #for xml in xml_files[1:]:
        #    self.xml = xml
        #    for pkg,mtd,result,log in self.__read():
        #        if result == self.PASS:
        #            if self.PASS in self.data[pkg]:
        #                self.data[pkg][self.PASS][mtd] = log
        #            else: self.data[pkg][self.PASS] = {mtd:log}
        #            self.data[pkg][self.FAIL].pop(mtd)
        #        elif result == self.FAIL:
        #            self.data[pkg][self.FAIL][mtd] = log
        #        else:
        #            continue