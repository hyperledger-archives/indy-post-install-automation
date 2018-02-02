"""
Created on Nov 24, 2017

@author: nhan.nguyen

Containing class for Test Runner.
"""

import os
import glob
import sys
import inspect
import importlib
import argparse
import multiprocessing
import reporter
from utilities import utils, constant, result
from utilities.test_scenario_base import TestScenarioBase


class TestRunner:
    __default_dir = os.path.dirname(os.path.abspath(__file__))
    __test_script_dir = __default_dir + "/test_scripts"
    __reporter_dir = __default_dir + "/reporter.py"

    def __init__(self):
        self.__args = None
        self.__catch_arg()
        self.__lst_json_files = []
        self.__lst_log_files = []
        pass

    def run(self):
        """
        Run all test scenario and then execute reporter if -html flag exist.
        """
        list_test_scenarios = self.__get_list_scenarios_in_folder()

        if not list_test_scenarios:
            utils.print_error(
                "\n{}\n".format(constant.ERR_CANNOT_FIND_ANY_TEST_SCENARIOS))
            exit(1)

        (tests_pass, tests_fail) = self.__execute_tests(list_test_scenarios)

        complete_message = constant.INFO_TEST_PASS_FAIL.format(
            tests_pass, tests_fail)

        print(complete_message)

        self.__execute_reporter()

    def __catch_arg(self):
        """
        Catch args for TestRunner in sys.argv.
        """
        arg_parser = argparse.ArgumentParser()
        arg_parser.add_argument("-d", "--directory", dest="directory",
                                default="", nargs="?",
                                help="directory of test "
                                     "scenarios (not recursive)")
        arg_parser.add_argument("-rd", "--recur_directory",
                                dest="recur_directory", default="", nargs="?",
                                help="directory of test scenarios (recursive)")
        arg_parser.add_argument("-t", "--timeout", dest="timeout", type=float,
                                help="timeout for each "
                                     "scenario (default: 300s)",
                                default=300, nargs="?")
        arg_parser.add_argument("-html", "--html_report", dest="report",
                                action="store_true", default=False,
                                help="if this flag is missing, html "
                                     "report would not be generated")
        arg_parser.add_argument("-l", "--keep_log", action="store_true",
                                help="keep all log file")
        self.__args = arg_parser.parse_args()
        if self.__args.timeout <= 0.0:
            print("Invalid timeout!")
            exit(1)

    def __execute_tests(self, lst_tests):
        """
        Execute all test case and collect the number of tests and pass.

        :param lst_tests:
        :return: number of tests pass and fail
        """
        tests_pass = tests_fail = 0
        queue_of_result = multiprocessing.Queue()
        for test in lst_tests:
            process = multiprocessing.Process(
                target=TestRunner.__helper_execute_test,
                kwargs={"test_cls": test,
                        "time_out": self.__args.timeout,
                        "channel": queue_of_result})
            process.start()
            process.join()
            temp_result = {}
            if not queue_of_result.empty():
                temp_result = queue_of_result.get_nowait()

            if "status" in temp_result:
                if temp_result["status"] == result.Status.PASSED:
                    tests_pass += 1
                else:
                    tests_fail += 1

            if "json_path" in temp_result:
                self.__lst_json_files.append(temp_result["json_path"])

            if "log_path" in temp_result:
                self.__lst_log_files.append(temp_result["log_path"])

        return tests_pass, tests_fail

    def __execute_reporter(self):
        """
        Execute html_reporter if -html flag is exist in sys.argv.
        """
        if not self.__args.report:
            return
        reporter.HTMLReporter().generate_report_from_file(
            self.__lst_json_files)

    def __get_list_scenarios_in_folder(self):
        """
        Get all scenario in folder.
        Recursive to sub folder if "-rd" argument appear in sys.argv.
        :return: list test scenarios.
        """
        # If both directory and recur_directory are exist
        # then show "Invalid command" and exit.
        if self.__args.directory is not "" \
                and self.__args.recur_directory is not "":
            utils.print_error("\n{}\n".format(constant.ERR_COMMAND_ERROR))
            exit(1)
        recursive = False

        start_directory = ""
        if self.__args.directory is not "":
            start_directory = self.__args.directory
        elif self.__args.recur_directory is not "":
            start_directory = self.__args.recur_directory
            recursive = True

        if not start_directory:
            start_directory = TestRunner.__test_script_dir

        if not os.path.exists(start_directory):
            utils.print_error(
                "\n{}\n".format(constant.ERR_PATH_DOES_NOT_EXIST.
                                format(start_directory)))
            exit(1)

        list_files = []
        if start_directory.endswith(".py"):
            list_files = [start_directory]
        else:
            try:
                if recursive:
                    for directory, _, _ in os.walk(start_directory):
                        list_files.extend(glob.glob(os.path.join(directory,
                                                                 "*.py")))
                else:
                    list_files.extend(glob.glob(os.path.join(start_directory,
                                                             "*.py")))
            except OSError:
                pass

        list_test_scenarios = []
        for file in list_files:
            sys.path.append(os.path.dirname(os.path.abspath(file)))
            test_module = \
                importlib.import_module(os.path.basename(file).replace(".py",
                                                                       ""))
            for name, cls in inspect.getmembers(test_module, inspect.isclass):
                if cls is not TestScenarioBase \
                        and issubclass(cls, TestScenarioBase):
                    list_test_scenarios.append(cls)

        return list_test_scenarios

    @staticmethod
    def __helper_execute_test(test_cls, channel, time_out):
        """
        Execute test case in a sub-process and send result to parent process

        :param test_cls: the test class the will be executed.
        :param channel: a side of pipe to communicate with parent process.
        :param time_out: time out of test case
        """
        test_case = test_cls()
        test_case.execute_scenario(time_out=time_out)
        temp = {}
        if hasattr(test_case, "test_result"):
            temp["status"] = test_case.test_result.get_test_status()
            temp["json_path"] = test_case.test_result.get_json_file_path()
            temp["log_path"] = test_case.logger.get_log_file_path()

        channel.put_nowait(temp)


if __name__ == "__main__":
    TestRunner().run()
