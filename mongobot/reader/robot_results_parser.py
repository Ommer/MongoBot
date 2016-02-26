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


    def _parse_suite(self, suite):
        logger.debug('Parsing suite "%s"', suite.name)
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
        # suite_doc['tests'] = suite.tests  

        suite_doc['stats_total'] = suite.statistics.all.total
        suite_doc['stats_passed'] = suite.statistics.all.passed
        suite_doc['stats_failed'] = suite.statistics.all.failed
        suite_doc['stats_critical_total'] = suite.statistics.critical.total
        suite_doc['stats_critical_passed'] = suite.statistics.critical.passed
        suite_doc['stats_critical_failed'] = suite.statistics.critical.failed

        return suite_doc

    def _format_robot_timestamp(self, timestamp):
        return datetime.strptime(timestamp, '%Y%m%d %H:%M:%S.%f')
