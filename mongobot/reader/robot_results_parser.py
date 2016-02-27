import logging
from datetime import datetime
import re

from bson import ObjectId 
from robot.api import ExecutionResult

logger = logging.getLogger(__name__)

class RobotResultsParser(object):

    
    def __init__(self, xml_file, include_keywords=False, db=None, run_name=''):
        self.xml_file = xml_file
        self.test_run = ExecutionResult(xml_file, include_keywords=include_keywords)
        self.test_run_id = ObjectId()
        run_name = 'run_%s' % datetime.utcnow().strftime('%Y_%m_%d') \
                   if not run_name else run_name
        self.test_run_doc = { '_id': ObjectId(), 
                              'imported_at': datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S'),
                              'run_name': run_name
                              }
        logger.info('Parsing xml file for run %s' % run_name)
        # inser run_id into runs collection 


    def traverse_suites(self):
        self._traverse_suites(self.test_run.suite)


    def _traverse_suites(self, suite):
        """ Recusivelly iterate through suites hierarchy""" 

        logger.debug("traversing suite '%s'", suite.longname)
        suite_doc = self._parse_suite(suite)
        # insert suite_doc into suites collection 
        pass 

        if not suite.suites and suite.tests:
            logger.debug('Suite "%s" has %d test cases' % (suite.name, len(suite.tests)))
            # for each test in suite.tests
            #     parse test and add it to tests collection
            # push suite_doc['path'] to test_runs document
            pass
            return 

        for child_suite in suite.suites:
            self._traverse_suites(child_suite)


    def _parse_suite(self, suite):
        logger.info('Parsing suite "%s"', suite.longname)

        suite_doc = {}
        suite_doc['name'] = suite.name 
        suite_doc['longname'] = suite.longname
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
        #
        # formatting all test cases in dic
        #
        tests = self._get_tests(suite)
        for test in tests:
          print self._parse_test(test)
        
        suite_doc['path'] = ','+re.sub(r'\.', ',', suite.longname)+','
        suite_doc['run_id'] = self.test_run_id

        return suite_doc

    #
    # get all tests from all suites
    # return list of test cases
    #
    def _get_tests(self,suite,tests=[]):

        if suite.tests:
          tests += suite.tests

        if not suite.tests:
            [self._get_tests(s,tests) for s in suite.suites]

        return tests

    #
    # return test in dictionary 
    #
    def _parse_test(self,test):
        logger.info('Parsing test: %s' % test.name) 
        
        test_doc = {}
        test_doc['doc']         = test.doc 
        test_doc['elapsedtime'] = test.elapsedtime
        test_doc['endtime']     = self._format_robot_timestamp(test.endtime).\
                                  strftime('%Y-%m-%d %H:%M:%S')
        test_doc['starttime'] = self._format_robot_timestamp(test.starttime).\
                                  strftime('%Y-%m-%d %H:%M:%S')      
        test_doc['tags']         = test.tags
        test_doc['status']      = test.status
        test_doc['test_id']     = test.id
        test_doc['keywords']    = test.keywords
        test_doc['message']     = test.message
        test_doc['passed']      = test.passed
        test_doc['critical']    = test.critical
        test_doc['longname']    = test.longname
        test_doc['name']        = test.name
        test_doc['parent']      = test.parent
        test_doc['timeout']     = test.timeout

        return test_doc

    def _format_robot_timestamp(self, timestamp):
        return datetime.strptime(timestamp, '%Y%m%d %H:%M:%S.%f')
