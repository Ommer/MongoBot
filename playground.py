import sys
import logging
from datetime import datetime
import json

from robot.api import ExecutionResult

from mongobot.reader.robot_results_parser import RobotResultsParser



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

parser = RobotResultsParser(sys.argv[1])
suite = parser.test_run.suite
doc = parser._parse_suite(suite)

print json.dumps(doc, indent=4, sort_keys=True)