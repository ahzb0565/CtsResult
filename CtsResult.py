"""
Usage:
y = CtsResult.CtsResult(CtsParser)
y.summary_report()

CtsParser is an Object of CtsParser
"""
from Parser import CsvParser, XmlParser

class Result(object):
    def __init__(self):
        """Parse all result by pkgs. This is the base of CtsReasult class.
        """
        self.data = None
        self.pakgs = None
        self.PASS,self.FAIL,self.NOTEXECUTED = "pass","fail","notexecuted"
        self.csv_parser = CsvParser
        self.xml_parser = XmlParser

    def translate_xmls(self,*xmls):
        parser = self.xml_parser()
        parser.translate(*xmls)
        self.data = parser.data
        self.pkgs = self.data.keys()

    def translate_csvs(self,*csv,valid_column = None):
        parser = self.csv_parser()
        parser.translate(*csv,valid_column)
        self.data = parser.data
        self.pkgs = self.data.keys()

    def pkg_summary(self,pkg):
        """Return the summary by specific pkg. total,pass,fail,notExecuted"""
        p = len(self.data[pkg][self.PASS]) if self.data[pkg].has_key(self.PASS) else 0
        f = len(self.data[pkg][self.FAIL]) if self.data[pkg].has_key(self.FAIL) else 0
        n = len(self.data[pkg][self.NOTEXECUTED]) if self.data[pkg].has_key(self.NOTEXECUTED) else 0
        return p+f+n,p,f,n
    def search_pkg_result(self,pkg,result):
        if pkg not in self.pkgs:
            raise Exception("Can't find pkg %s"%pkg)
        if not self.data[pkg].has_key(result):
            return []
        return self.data[pkg][result].keys()
    def pkg_failed_cases(self,pkg):
        """Get failed cases list by specific pkg"""
        return self.search_pkg_result(pkg,self.FAIL)
    def pkg_passed_cases(self,pkg):
        """Get passed cases list by specific pkg"""
        return self.search_pkg_result(pkg,self.PASS)
    def pkg_notExecuted_cases(self,pkg):
        """Get notExecuted cases list by specific pkg"""
        return self.search_pkg_result(pkg,self.NOTEXECUTED)
    def get_log(self,pkg,method):
        """Get the log by specific pkg and method.
        Return None If log is empty or case not failed."""
        if self.data.has_key(pkg) and self.data[pkg].has_key(self.FAIL) and self.data[pkg][self.FAIL].has_key(method):
            return self.data[pkg][self.FAIL][method]

class CtsResult(Result):
    """
    example:
    y = CtsResult()
    y.translate_csv(csv) or y.translate_xmls(xml1,xml2,...)
    y.summary()
    """
    def __init__(self):
        Result.__init__(self)
        #self.pkgs = self.data.keys()
        self.summary_base_str = "Total: %5d, Pass: %5d, Fail: %5d, notExecuted: %5d"
    def summary(self):
        """Get the number of total/pass/fail/notExecuted."""
        t,p,f,n = 0,0,0,0
        for pkg in self.pkgs:
            result = self.pkg_summary(pkg)
            p += result[1]
            f += result[2]
            n += result[3]
        t = p+f+n
        return t,p,f,n
    def summary_report(self):
        """Print CTS report"""
        self.pkgs_report()
        print "-" * 50
        print "Summary:\n"+ self.summary_base_str%self.summary()
    def pkgs_report(self):
        """Print report of all pkgs."""
        for pkg in self.pkgs:
            t,p,f,n = self.pkg_summary(pkg)
            print "%-50s : %s"%(pkg,self.summary_base_str%(t,p,f,n))
    def search_all_by_result(self,result):
        ret = {}
        for pkg in self.pkgs:
            r = self.search_pkg_result(pkg,result)
            if not r: continue
            ret.update({pkg:r})
        return ret
    def failed_cases(self):
        """Return all failed cases by pkgs
        ret = {pkg1:[case1,case2], ...}
        """
        return self.search_all_by_result(self.FAIL)
    def passed_cases(self):
        """Return all passed cases by pkgs
        ret = {pkg1:[case1,case2], ...}
        """
        return self.search_all_by_result(self.PASS)
    def notExecuted_cases(self):
        """Return all notExecuted cases by pkgs
        ret = {pkg1:[case1,case2], ...}
        """
        return self.search_all_by_result(self.NOTEXECUTED)