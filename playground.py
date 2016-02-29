import sys
import logging
from datetime import datetime
import json
import pprint

from robot.api import ExecutionResult

from mongobot.reader.robot_results_parser import RobotResultsParser

logging.basicConfig(level=logging.INFO)

logging.basicConfig(level=logging.DEBUG)

# class RobotResultsParser(object):

#     def __init__(self, xml_file, include_keywords=False):
#         self.test_run = ExecutionResult(xml_file, include_keywords=include_keywords)

#     def demo(self):
#         # must rewrite it recursivelly 
#         print '------------------'
#         parent_suite = self.test_run.suite
#         print 'Parent Suite: %s' % parent_suite.name
#         for child_suite in parent_suite.suites:
#             print child_suite.name
# parser = RobotResultsParser('output3.xml')
# parser.demo()

parser = RobotResultsParser(sys.argv[1], include_keywords=True)
suite = parser.test_run.suite
# doc = parser._parse_test(suite.suites[0].tests[0])
doc = parser._parse_suite(suite)

# keyowrds = suite.tests[0].keywords
# print keyowrds

print pprint.pprint(doc, indent=4)

parser.traverse_suites()
# parser.suite_test_cases()