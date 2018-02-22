"""
Created on Nov 12, 2017

@author: nghia.huynh

Containing all functions and classes to make HTML report.
"""
import os
import json
import socket
import platform
import glob
import subprocess
import errno
import argparse
import time


def get_version(program: str) -> str:
    """
    Return version of a program.

    :param program: program's name.
    :return: version.
    """
    cmd = "dpkg -l | grep '{}'".format(program)
    process = subprocess.Popen([cmd], shell=True, stdout=subprocess.PIPE,
                               stdin=subprocess.PIPE)
    (out, _) = process.communicate()
    result = out.decode()
    version = result.split()

    if len(version) >= 3:
        if version[1] == program:
            return version[2]
    return "Cannot find version for '{}'".format(program)


class JsonSummaryReport:
    __default_dir = os.path.dirname(os.path.abspath(__file__))

    __json_dir = __default_dir + "/test_output/test_results/"

    __report_dir = __default_dir + "/reporter_summary_report/"

    __dependencies = ["indy-plenum", "indy-node", "indy-anoncreds", "sovrin"]

    __SYSTEM = "system_info"
    __OS = "os"
    __HOST_NAME = "host_name"
    __RESULTS = "test_results"
    __SUMMARY = "summary"
    __TOTAL_TESTS = "total_tests"
    __PASSED_TESTS = "passed_tests"
    __FAILED_TESTS = "failed_tests"
    __DURATION = "duration"

    def __init__(self):
        JsonSummaryReport.__init_report_folder()
        self.__json_content = dict()

    def generate_report_from_file(self, json_files: list):
        """
        Generate report from an list of json files.

        :param json_files:
        """
        report_file_name = JsonSummaryReport.__make_report_name()

        # Write to file.
        summary_json_file = self.__report_dir + report_file_name + ".json"
        self.__make_system_info()
        self.__make_result(json_files)

        # With json summary to file.
        with open(summary_json_file, "w+") as json_summary:
            json.dump(self.__json_content, json_summary,
                      ensure_ascii=False, indent=2, sort_keys=True)

    def generate_report_from_filter(self, file_filter):
        """
        Generate report form filter.

        :param file_filter:
        :return:
        """
        file_filter = "*" if not file_filter else file_filter
        list_file_name = glob.glob(self.__json_dir + file_filter + ".json")
        if not list_file_name:
            print("Cannot find any json at {}".format(
                JsonSummaryReport.__json_dir))
            return

        self.generate_report_from_file(list_file_name)

    def __make_system_info(self):
        system_info = dict()
        system_info[JsonSummaryReport.__HOST_NAME] = socket.gethostname()
        system_info[JsonSummaryReport.__OS] = (platform.system() +
                                               platform.release())

        for dependency in JsonSummaryReport.__dependencies:
            system_info[dependency] = get_version(dependency)

        self.__json_content[JsonSummaryReport.__SYSTEM] = system_info

    def __make_result(self, list_files):
        test_results = list()
        test_passed = test_failed = 0
        total = len(list_files)
        duration = 0
        for file in list_files:
            test_result = json.load(open(file))
            if test_result["result"].lower() == "passed":
                test_passed += 1
            else:
                test_failed += 1
            duration += test_result["duration"]
            test_results.append(test_result)

        # Make summary.
        summary = dict()
        summary[JsonSummaryReport.__TOTAL_TESTS] = total
        summary[JsonSummaryReport.__PASSED_TESTS] = test_passed
        summary[JsonSummaryReport.__FAILED_TESTS] = test_failed
        summary[JsonSummaryReport.__DURATION] = duration

        self.__json_content[JsonSummaryReport.__SUMMARY] = summary
        self.__json_content[JsonSummaryReport.__RESULTS] = test_results

    @staticmethod
    def __make_report_name() -> str:
        """
        Generate report name.
        :return: report name.
        """
        name = "Summary_{}".format(str(time.strftime("%Y-%m-%d_%H-%M-%S")))

        return name

    @staticmethod
    def __init_report_folder():
        """
        Create reporter_summary_report directory if it not exist.
        :raise OSError.
        """
        try:
            os.makedirs(JsonSummaryReport.__report_dir)
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise e


class HTMLReporter:
    __default_dir = os.path.dirname(os.path.abspath(__file__))

    __json_dir = __default_dir + "/test_output/test_results/"

    __report_dir = __default_dir + "/reporter_summary_report/"

    __head = """<html>
            <head>
             <meta http-equiv="Content-Type" content="text/html;
             charset=windows-1252">
                <title>Summary Report</title>
                <style type="text/css">table {
                    margin-bottom: 10px;
                    border-collapse: collapse;
                    empty-cells: show
                }

                th, td {
                    border: 1px solid #009;
                    padding: .25em .5em
                }

                th {
                    text-align: left
                }

                te {
                    border: 1px solid #009;
                    padding: .25em .5em
                    text-align: left
                    color_name: red
                }

                td {
                    vertical-align: top
                }

                table a {
                    font-weight: bold
                }

                .stripe td {
                    background-color: #E6EBF9
                }

                .num {
                    text-align: right
                }

                .passedodd td {
                    background-color: #0A0
                }

                .passedeven td {
                    background-color: #0A0
                }

                .skippedodd td {
                    background-color: #DDD
                }

                .skippedeven td {
                    background-color: #CCC
                }

                .failedodd td, .attn {
                    background-color: #D00
                }

                .failedeven td, .stripe .attn {
                    background-color: #D00
                }

                .stacktrace {
                    white-space: pre;
                    font-family: monospace
                }

                .totop {
                    font-size: 85%;
                    text-align: center;
                    border-bottom: 2px solid #000
                }</style>
            </head>"""

    __end_file = """</html>"""

    __suite_name = """<h3>{}</h3>"""

    __configuration_table = """<table id="configuration">
            <tbody>
            <tr>
                <th>Run machine</th>
                <td>{}</td>
            </tr>
            <tr>
                <th>OS</th>
                <td>{}</td>
            </tr>
            <tr>
                <th>indy - plenum</th>
                <td>{}</td>
            </tr>
             <tr>
                <th>indy - anoncreds</th>
                <td>{}</td>
            </tr>
            <tr>
                <th>indy - node</th>
                <td>{}</td>
            </tr>
            <tr>
                <th>sovrin</th>
                <td>{}</td>
            </tr>
            </tbody>
        </table>"""

    __statictics_table = """<table border='1' width='800'>
            <tbody>
            <tr>
                <th>Test Plan</th>
                <th># Passed</th>
                <th># Failed</th>
                <th>Time (ms)</th>
            </tr>
            <tr>
                <td>{}</td>
                <td class="num">{}</td>
                <td class="num">{}</td>
                <td class="num">{}</td>
            </tr>
            </tbody>
        </table>"""

    __passed_testcase_template = """<tr class="passedeven">
                                           <td rowspan="1">{}</td>
                                           <td>Passed</td>
                                           <td rowspan="1">{}</td>
                                           <td rowspan="1">{}</td>
                                       </tr>"""

    __passedodd_testcase_template = """<tr class="passedodd">
                                               <td rowspan="1">{}</td>
                                               <td>Passed</td>
                                               <td rowspan="1">{}</td>
                                               <td rowspan="1">{}</td>
                                           </tr>"""

    __failed_testcase_template = """<tr class="failedeven">
                                            <td rowspan="1">{}</td>
                                            <td><a href='#{}'s>Failed</a></td>
                                            <td rowspan="1">{}</td>
                                            <td rowspan="1">{}</td>
                                        </tr>"""

    __failedodd_testcase_template = """<tr class="failedodd">
                                                <td rowspan="1">{}</td>
                                                <td><a href='#{}'>Failed</a>
                                                </td>
                                                <td rowspan="1">{}</td>
                                                <td rowspan="1">{}</td>
                                            </tr>"""

    __summary_head = """<h2>Test Summary</h2>
            <table id="summary" border="1">
            <thead>
            <tr>
                <th>Test Case</th>
                <th>Status</th>
                <th>Start Time</th>
                <th>Duration (ms)</th>
            </tr>
            </thead>"""

    __go_to_summary = """<a href = #summary>Back to summary.</a>"""

    __begin_summary_content = """
            <tbody>
            <tr>
                <th colspan="4"></th>
            </tr>"""

    __end_summary_content = """</tbody>"""

    __end_table = """ </table> """

    __passed_testcase_table = """ """

    __failed_testcase_table = """ """

    __test_log_head = """<h2>Test Execution Logs</h2>"""

    __table_test_log = """<h3 id = "{}">{}</h3>
                            <table id="execution_logs"
                            border='1' width='800'>"""

    __table_test_log_content = """ """

    __passed_test_log = """
            <tr>
                <td><font color="green">{} : {} :: {}</font></td>
            </tr>"""

    __failed_test_log = """
            <tr>
                <td><font color="red">{} : {} :: {}
                <br>Traceback: {}</br>
                </font>
                </td>
            </tr>
            """
    # Define some variable to support generate summary json file.
    __system_info = '{{"system_info":{{"run_machine":"{}","OS":"{}",' \
                    '"indy_plenum":"{}","indy_anoncreds":"{}",' \
                    '"indy_node":"{}","sovrin":"{}"}}}}'
    __test_plan = '{{"testplan":{{"total":{},"Passed":{},"Failed":{},' \
                  '"Duration":{}}}}}'
    passed = 0
    failed = 0
    time_duration = 0
    total_testcases = 0

    def make_suite_name(self, suite_name):
        """
        Generating the statistics table.
        :param suite_name:
        """
        self.__suite_name = self.__suite_name.format(suite_name)

    def make_configurate_table(self):
        """
        Generating the configuration table.
        """
        self.__configuration_table = \
            self.__configuration_table.format(socket.gethostname(),
                                              platform.system() +
                                              platform.release(),
                                              get_version("indy-plenum"),
                                              get_version("indy-anoncreds"),
                                              get_version("indy-node"),
                                              get_version("sovrin"))

    def make_report_content_by_list(self, list_json: list, suite_name):
        """
        Generating the report content by reading all json file
        within the inputted path
        :param list_json:
        :param suite_name:
        """
        if not list_json:
            return

        list_json.sort()
        self.total_testcases = len(list_json)
        for js in list_json:
            with open(js) as json_file:
                json_text = json.load(json_file)

                # summary item
                testcase = json_text['testcase']
                result = json_text['result']
                starttime = json_text['starttime']
                duration = json_text['duration']

                # statictic Table items
                self.time_duration = self.time_duration + int(duration)
                if result == "Passed":
                    self.passed = self.passed + 1
                    if self.passed % 2 == 0:
                        temp_testcase = self.__passed_testcase_template
                    else:
                        temp_testcase = self.__passedodd_testcase_template
                    temp_testcase = temp_testcase.format(testcase, starttime,
                                                         str(duration))

                    # Add passed test case into  table
                    self.__passed_testcase_table = \
                        self.__passed_testcase_table + temp_testcase

                elif result == "Failed":
                    self.failed = self.failed + 1
                    if self.passed % 2 == 0:
                        temp_testcase = self.__failed_testcase_template
                    else:
                        temp_testcase = self.__failedodd_testcase_template
                    temp_testcase = \
                        temp_testcase.format(testcase,
                                             testcase.replace(" ", ""),
                                             starttime, str(duration))

                    # Add failed test case into  table
                    self.__failed_testcase_table = \
                        self.__failed_testcase_table + temp_testcase

                    test_log = self.__table_test_log
                    test_log = test_log.format(testcase.replace(" ", ""),
                                               testcase)

                    self.__table_test_log_content = \
                        self.__table_test_log_content + test_log

                    # loop for each step
                    for i in range(0, len(json_text['teststeps'])):
                        step = json_text['teststeps'][i]['step']
                        status = json_text['teststeps'][i]['status']
                        if json_text['teststeps'][i]['status'] == "Passed":
                            temp = self.__passed_test_log.format(str(i + 1),
                                                                 step, status)
                        else:
                            message = json_text['teststeps'][i]['message']
                            temp = self.__failed_test_log.format(str(i + 1),
                                                                 step, status,
                                                                 message)

                        self.__table_test_log_content = \
                            self.__table_test_log_content + temp

                    self.__table_test_log_content = \
                        self.__table_test_log_content + self.__end_table + \
                        self.__go_to_summary

        self.__statictics_table = self.__statictics_table.format(
            suite_name,
            str(self.passed),
            str(self.failed),
            str(self.time_duration))

    def __init__(self):
        HTMLReporter.__init_report_folder()

    def generate_report_from_file(self, json_files: list):
        """
        Generate report from an list of json files.

        :param json_files:
        """
        print("Generating a html report...")
        report_file_name = HTMLReporter.__make_report_name()
        self.make_suite_name(report_file_name)
        self.make_configurate_table()
        self.make_report_content_by_list(json_files, report_file_name)

        # Write to file.
        print(("Refer to " + self.__report_dir + "{}.html").
              format(report_file_name))
        f = open((self.__report_dir + "{}.html").format(report_file_name), 'w')
        f.write(
            self.__head +
            self.__suite_name +
            self.__configuration_table +
            self.__statictics_table +
            self.__summary_head +
            self.__begin_summary_content +
            self.__passed_testcase_table +
            self.__end_summary_content +
            self.__begin_summary_content +
            self.__failed_testcase_table +
            self.__end_summary_content +
            self.__end_table +
            self.__test_log_head +
            self.__table_test_log_content +
            self.__end_file)

        f.close()

    def __generate_json_summary(self, list_json, summary_json_file):
        list_data = []
        list_json.sort()
        for js in list_json:
            data = open(js, "r").read()
            data = data + "\n"
            list_data.append(data)
        self.__write_result(list_data, summary_json_file)

    def __write_result(self, list_data, summary_json_file):
        summary_json = open(summary_json_file, "w")
        system_info = self.__system_info.format(socket.gethostname(),
                                                platform.system() +
                                                platform.release(),
                                                get_version("indy-plenum"),
                                                get_version("indy-anoncreds"),
                                                get_version("indy-node"),
                                                get_version("sovrin"))
        test_plan = self.__test_plan.format(self.total_testcases, self.passed,
                                            self.failed, self.time_duration)
        summary_json.write(system_info + "\n" + test_plan + "\n")
        summary_json.writelines(list_data)
        summary_json.close()

    def generate_report_from_filter(self, file_filter):
        """
        Generate report form filter.

        :param file_filter:
        :return:
        """
        file_filter = "*" if not file_filter else file_filter
        list_file_name = glob.glob(self.__json_dir + file_filter + ".json")
        if not list_file_name:
            print("Cannot find any json at {}".format(HTMLReporter.__json_dir))
            return

        self.generate_report_from_file(list_file_name)

    @staticmethod
    def __make_report_name() -> str:
        """
        Generate report name.
        :return: report name.
        """
        name = "Summary_{}".format(str(time.strftime("%Y-%m-%d_%H-%M-%S")))

        return name

    @staticmethod
    def __init_report_folder():
        """
        Create reporter_summary_report directory if it not exist.
        :raise OSError.
        """
        try:
            os.makedirs(HTMLReporter.__report_dir)
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise e


if __name__ == "__main__":
    json_reporter = JsonSummaryReport()
    htmt_reporter = HTMLReporter()
    # Get argument from sys.argv to make filters
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument("-n", "--name", dest="name", nargs="?",
                            default=None, help="filter json file by name")
    args = arg_parser.parse_args()
    json_filter = args.name

    # Generate a html report
    json_reporter.generate_report_from_filter(json_filter)
    htmt_reporter.generate_report_from_filter(json_filter)
