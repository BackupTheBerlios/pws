import sys, unittest, StringIO
from lib.Interface import BaseInterface

class BaseInterfaceTestCase(unittest.TestCase):
    def setUp(self):
        self.interface = BaseInterface()
        self.old_stdout = sys.stdout
        self.output = StringIO.StringIO()
        sys.stdout = self.output

    def tearDown(self):
        self.output.close()
        sys.stdout = self.old_stdout

    def countString(self, count, maxcount):
        countStr = ""
        for c in range(1, count + 1):
            ellipsis = "..."
            if c == maxcount:
                ellipsis = ""
            countStr += "%d%s" % (c, ellipsis)

        return countStr
    
    def test_doCountPin1(self):
        self.interface._doCount(1, "PIN_COUNTS")
        self.assertEqual(self.output.getvalue(), "1...\n")

    def test_doCountPin2(self):
        self.interface._doCount(2, "PIN_COUNTS")
        self.assertEqual(self.output.getvalue(), "1...2...\n")

    def test_doCountPin3(self):
        self.interface._doCount(3, "PIN_COUNTS")
        self.assertEqual(self.output.getvalue(), "1...2...3\n")

    def test_doCountCountout1(self):
        self.interface._doCount(1, "COUNTOUT")
        self.assertEqual(self.output.getvalue(), "1...\n")

    def test_doCountCountout5(self):
        count = 5
        self.interface._doCount(count, "COUNTOUT")
        self.assertEqual(self.output.getvalue(),
                         "%s\n" % self.countString(count, 10))

    def test_doCountCountout10(self):
        count = 10
        self.interface._doCount(count, "COUNTOUT")
        self.assertEqual(self.output.getvalue(),
                         "%s\n" % self.countString(count, 10))
        
suite = unittest.TestLoader().loadTestsFromTestCase(BaseInterfaceTestCase)
unittest.TextTestRunner(verbosity=2).run(suite)
        
