import os
import sys
import time
import pytest
import reporter
from utilities import result, utils


def pytest_addoption(parser):
    group = parser.getgroup('terminal reporting')
    group.addoption("--keeplog", action="store_true",
                    help="keep all log no matter what test's status")


def pytest_namespace():
    return {"current_exception": None, 'current_id': None}


def pytest_runtest_logreport(report):
    """
    Catch and save the log if test failed of option keep log (-l) exist.

    :param report: report of pytest that contains log.
    """
    if report.failed or '--keeplog' in sys.argv:
        log_dir = utils.get_project_path() + "/test_output/log_files/"
        utils.create_folder(log_dir)

        # Get test's name.
        cur_time = str(time.strftime("%Y-%m-%d_%H-%M-%S"))
        path_to_test = report.nodeid.split("::")[0]
        test_name = os.path.basename(path_to_test)
        if pytest.current_id:
            test_name = pytest.current_id

        log_path = "{}{}_{}.log".format(log_dir, test_name, cur_time)

        log = ""
        if report.longrepr:
            for line in report.longreprtext.splitlines():
                log += "\n" + line

        for header, content in report.sections:
            log += "\n" + (' {0} '.format(header).center(80, '-'))
            log += "\n" + content

        with open(log_path, "w") as log_file:
            log_file.write(log)


@pytest.fixture(scope="session", autouse=True)
def add_indy_system_info_to_metadata(metadata):
    sovrin_system = ["indy-plenum", "indy-node", "indy-anoncreds", "sovrin",
                     "libindy", "libsodium18:amd64", "libindy-crypto",
                     "libsqlite0"]

    info = ""
    for k in sovrin_system:
        sub_info = "[{}-{}]".format(k, utils.get_version(k))
        info = "{} {}".format(info, sub_info)

    metadata["Sovrin system"] = info
    del metadata["Packages"]
    del metadata["Plugins"]


@pytest.fixture(scope="session", autouse=True)
def make_json_summary(request):
    """
    Make json summary report after session if there is a option to generate
    html report.

    :param request:
    """
    yield
    if request.config.getoption("htmlpath") is not None:
        reporter.JsonSummaryReport().generate_report_from_file(
            result.Result.result_of_all_tests)


@pytest.hookimpl(hookwrapper=True, tryfirst=True)
def pytest_runtest_setup(item):
    pytest.current_exception = None
    pytest.current_id = None

    def get_id(item_name: str):
        if "[" and "]" in item_name:
            begin = item_name.index("[")
            end = item_name.index("]")
            return item_name[begin + 1: end]
        elif not item_name == "test":
            return item_name
        return None
    pytest.current_id = get_id(item.name)
    yield


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_call():
    outcome = yield
    exinfo = outcome._excinfo
    if exinfo:
        pytest.current_exception = "{}: {}".format(exinfo[0].__name__,
                                                   str(exinfo[1]))
