import csv
import os
from xml.dom import minidom

class Parser:
    """Base class of parser.
    x = Parser()
    x.translate(f)
    x.get_data()
    """
    def __init__(self):
        self.result_name = ""
        self.data = {}
        self.PASS, self.FAIL, self.NOTEXECUTED = "pass", "fail", "notexecuted"
    def translate(self,f):
        """Translate to the format like: {pkg1:{result{class.method:log)}"""
        pass
    def get_data(self):
        return self.data
    def get_result_name(self):
        return self.result_name

def csv_generator(csv_file):
    """A simple generator to read csv file. And use csv.DictReader."""
    try:
        f = open(csv_file,"rb")
        reader = csv.DictReader(f)
        for line in reader:
            #print line
            yield line
    except Exception,e:
        print str(e)
    finally:
        f.close()

class CsvParser(Parser):
    """
    CSV parser.
    x = Csv_parser()
    x.translate(csv,valid_column = VALID_VOLUMN) # VALID_VOLUME must follow self.default_valid_column
    x.get_data()
    """
    def __init__(self):
        Parser.__init__(self)
        self.csv_file = None
        #self.__data = {}
        self.generator = csv_generator
        self.default_valid_column = {"pkg":"Component","mtd":"Name","result":"Status","log":"Comment"}
    def __read(self,csv_file):
        print "Reading file ...%s"%csv_file
        return self.generator(csv_file)
    def translate(self,*csv_files,valid_column = None):
        """Translate result data to {pkg:{result:{method:log}}}
        valid_column = {"pkg":"Component","mtd":"Name","result":"Status","log":"Comment"}
        """
        #self.csv_file = csv_file
        #self.result_name = os.path.splitext(self.csv_file)[0]
        self.valid_column = valid_column if valid_column else self.default_valid_column
        self.data = {}
        for csv in csv_files:
            for line in self.__read(csv):
                pkg = line[self.valid_column["pkg"]].strip()
                mtd = line[self.valid_column["mtd"]].strip()
                result = line[self.valid_column["result"]].strip().lower()
                log = line[self.valid_column["log"]].strip()
                if pkg in self.data:
                    if result in self.data[pkg]:
                        self.data[pkg][result][mtd] = log
                    else:
                        self.data[pkg][result] = {mtd:log}
                else:
                    self.data[pkg] = {result:{mtd:log}}

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

class XmlParser(Parser):
    def __init__(self):
        Parser.__init__(self)
        self.xml = None
        self.generator = xml_generator
    def __read(self,xml):
        """Read source file"""
        xml_root = minidom.parse(xml).documentElement
        self.result_name = xml_root.getAttribute("testPlan")
        print "Reading file ... %s"%self.xml
        return self.generator(xml_root)
    def translate(self,*xml_files):
        """Translate to the format like: {pkg1:{result{class.method:log)}"""
        self.data = {}
        for xml in xml_files:
            for pkg,mtd,result,log in self.__read(xml):
                if pkg in self.data:
                    if result in self.data[pkg]:
                        self.data[pkg][result][mtd] = log
                    else:
                        self.data[pkg][result] = {mtd:log}
                else:
                    self.data[pkg] = {result:{mtd:log}}
    #def multi_translate(self,*xmls):
    #    """Some cts xml result have 3 loops. 
    #    This method is to merge and translate 3 loops' result to one.
    #    The xml_files arg should have sequence like: [loop1,loop2,loop3,...]
    #    """
    #    for xml in xmls:
    #        self.translate(xml)