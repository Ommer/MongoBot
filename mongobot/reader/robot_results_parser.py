import logging
from datetime import datetime

from robot.api import ExecutionResult

logger = logging.getLogger(__name__)

class RobotResultsParser(object):

    
    def __init__(self, xml_file, include_keywords=False, db=None):
        self.xml_file = xml_file
        self.test_run = ExecutionResult(xml_file, include_keywords=include_keywords)

    
    def xml_to_mongodb(self):
        pass


    def _traverse_suites(self, suite):
        """ Recusivelly iterate through suites hierarchy""" 

        logger.debug("traversing suite '%s'", suite.longname)
        suite_doc, tests = self._parse_suite(suite)
        # insert suite_doc into suites collection 
        pass 

        if not suite.suites and tests:
            # get all test cases and insert them to mongo 
            # update list of tests to suite doc
            pass
            return 

        for child_suite in suite.suites:
            self._traverse_suites(self, child_suite)
            

    def _parse_suite(self, suite):
        logger.info('Parsing suite "%s"', suite.longname)

        suite_doc = {}
        suite_doc['name'] = suite.name 
        suite_doc['longname'] = suite.longname
        suite_doc['imported_at'] = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
        suite_doc['starttime'] = self._format_robot_timestamp(suite.starttime).\
                                 strftime('%Y-%m-%d %H:%M:%S')
        suite_doc['endtime'] = self._format_robot_timestamp(suite.endtime).\
                               strftime('%Y-%m-%d %H:%M:%S')
        suite_doc['elapsedtime'] = suite.elapsedtime
        suite_doc['passed'] = suite.passed
        suite_doc['doc'] = suite.doc
        suite_doc['status'] = suite.status
        suite_doc['message'] = suite.message
        suite_doc['stat_message'] = suite.stat_message
        suite_doc['test_count'] = suite.test_count 

        suite_doc['stats'] = \
                  [  {'type': 'all', 
                      'total':  suite.statistics.all.total,
                      'passed': suite.statistics.all.passed,
                      'failed': suite.statistics.all.failed
                     },
                     {'type': 'critical', 
                      'total':  suite.statistics.critical.total,
                      'passed': suite.statistics.critical.passed,
                      'failed': suite.statistics.critical.failed
                     },
                  ]

        suite_tests = suite.tests  
        return suite_doc, suite_tests


    def _format_robot_timestamp(self, timestamp):
        return datetime.strptime(timestamp, '%Y%m%d %H:%M:%S.%f')
