"""
Usage:
import CtsCsvParser
x = CtsCsvParser.CsvParser()
x.translate(CSV_FILE,VALID_COLUMN)
x.get_data()
"""

import csv,os
import ParserBase

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

class CsvParser(ParserBase.Parser):
    """
    CSV parser.
    x = Csv_parser()
    x.translate(csv,valid_column = VALID_VOLUMN) # VALID_VOLUME must follow self.default_valid_column
    x.get_data()
    """
    def __init__(self):
        ParserBase.Parser.__init__(self)
        self.csv_file = None
        #self.__data = {}
        self.generator = csv_generator
        self.default_valid_column = {"pkg":"Component","mtd":"Name","result":"Status","log":"Comment"}
    def __read(self):
        print "Reading file ...%s"%self.csv_file
        return self.generator(self.csv_file)
    def translate(self,csv_file,valid_column = None):
        """Translate result data to {pkg:{result:{method:log}}}
        valid_column = {"pkg":"Component","mtd":"Name","result":"Status","log":"Comment"}
        """
        self.csv_file = csv_file
        self.result_name = os.path.splitext(self.csv_file)[0]
        self.valid_column = valid_column if valid_column else self.default_valid_column
        self.data = {}
        for line in self.__read():
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