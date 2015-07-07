"""
Usage:
z = CtsCompare()
z.load(x.get_data(),x.get_result_name())
z.load(y.get_data(),y.get_result_name())
z.load(x.get_data())
z.merge()
z.get_result_csv()
"""

import csv

class Compare:
    def __init__(self):
        self.data = {}
        self.tags = []
        self.PASS,self.FAIL,self.NOTEXECUTED,self.NA = "pass","fail","notexecuted","n/a"
    def load(self,result,tag = None):
        tag = tag if tag else "Result"+str(len(self.tags))
        print "Loading result %s"%tag
        if tag not in self.tags:
            self.tags.append(tag)
        for pkg in result:
            if pkg not in self.data:
                self.data[pkg] = {}
            for r in result[pkg]:
                for case in result[pkg][r]:
                    if case not in self.data[pkg]:
                        self.data[pkg][case] ={tag:r}
                    else: self.data[pkg][case][tag] = r
        #self.merge()
    def merge(self):
        for pkg in self.data:
            for case in self.data[pkg]:
                for tag in self.tags:
                    if tag not in self.data[pkg][case].keys():
                        self.data[pkg][case][tag] = self.NA
class CtsCompare(Compare):
    def __init__(self):
        Compare.__init__(self)
    #def merge_results(self,results):
    #    for result in results:
    #        self.load(result,tag)
    #    self.merge()
    def get_result_csv(self,csv_name = None):
        hashs = ["Package","Method"] + self.tags
        csv_name = csv_name if csv_name else "_".join(self.tags)
        #print csv_name
        try:
            f = open(csv_name+".csv","wb")
            writer = csv.writer(f)
            writer.writerow(hashs)
            for pkg in self.data:
                for case in self.data[pkg]:
                    rs = []
                    for tag in self.tags:
                        rs.append(self.data[pkg][case][tag])
                    writer.writerow([pkg,case] + rs)
            print "Result saved to %s.csv"%csv_name
        except Exception,e:
            print "get_result_csv exception:"
            print str(e)
        finally:
            f.close()
    def failed_compare(self):
        pass
    def passed_compare(self):
        pass
    def pkg_compare(self):
        pass
