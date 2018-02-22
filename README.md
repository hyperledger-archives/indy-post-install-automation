# Indy Python wrapper test

This is a Python wrapper test for Indy, using pytest, a framework that makes building simple and scalable tests easy.
This Python wrapper test currently requires python 3.5 and base58 (required for testing signus only).

### Application Under Test
Python Wrapper - FFI based wrapper for native libindy that allows application development with python language.

Specification to API calls for are present as comments in interface parts of source code:
* https://github.com/hyperledger/indy-sdk/tree/master/libindy/include/ (libindy docs)
* https://github.com/hyperledger/indy-sdk/tree/master/wrappers/python/indy/ (python wrapper docs)

### Repository Structure
Indy Python wrapper test contains the following parts:
 
- test_scripts:
     - acceptance_tests: The Acceptance test procedure consists of the following tests:
          - check_connection_test.py
          - keyrings_wallets_test.py 
          - remove_and_add_role_test.py 
          - special_case_trust_anchor_role_test.py 
          - verify_messages_on_connection_test.py
     - functional_tests: storing the tests that located in the specific functional folders:
          - agent
          - anoncreds
          - crypto
          - ledger
          - misc (the miscellaneous tests that may not fit in a specific functional folder)
          - pairwise
          - pool
          - signus
          - wallet
           
- utilities:
     - common.py: Containing all functions that is common among test scenarios.
     - constant.py: Containing all constants that are necessary to execute test scenario.
     - logger.py: Containing classes to catch the log on console for writing to json file.
     - result.py: Containing classes to make the test result as a json.
     - step.py: Containing the classes to manage the list of test step and the step's information ( step name, step status, steps message).
     - test_scenario_base.py: Containing the test base class. All test scenario should inherit from this class. This class controls the work flow and hold some general test data for test scenarios that inherit it
     - utils.py: Containing all functions used by several test steps on test scenarios.

- reporter_summary_report: Containing the html report. (Will be generated after first run).
- test_output:  Will be generated after first run.
     - log_files: Containing the log files of each failed test case.
     - test_results: Containing the json result files of test case.

- reporter.py: Generate an HTML report to show the summary all the tests run during the same timeframe (example: all test run on 2017-11-16 would be in one report with that date). This would include tests that were run multiple times in a single day. And the report is stored in the 'reporter summary report' folder.

### How to run

After building successfully the Indy SDK for Python, you need to run the commands below so that could run the tests:

- Install base58 dependency with pip install: 
```
     python3.5 -m pip install base58
```
- Setup PYTHONPATH: 
```
    export PYTHONPATH=$PYTHONPATH:<your_repo_location>
```
- Install pytest:
```
    python3.5 -m pip install -U pytest
```
- Install pytest-html (a plugin for pytest that generates a HTML report for the test results):
```
    python3.5 -m pip install -U pytest-html
```
- Install pytest-timeout (py.test plugin to abort hanging tests):
```
    python3.5 -m pip install -U pytest-timeout
```

#### Then run:
- Run one test case:
```
    pytest <your_repo_location>/test_scripts/functional_tests/pool/refresh_pool_ledger_works_with_valid_data_test.py
```
- Run all test cases in a folder:
```
    pytest <your_repo_location>/test_scripts/functional_tests/pool --html=report.html --self-contained-html
```
- Run all test cases in the project:
``` 
    pytest <your_repo_location>/test_scripts --html=reportalltest.html --self-contained-html
```
- Run all test cases in the project with test timeout in second:
```
    pytest <your_repo_location>/test_scripts --html=timeouttest.html --self-contained-html --timeout=100
```

#### Generate the html report:
- Get the summary report for all the run:
```
    python3.5 <your_repo_location>/reporter.py
```
- Get the summary report for a group of test cases:
```
    python3.5 <your_repo_location>/reporter.py -n *wallet*
```
- Get the summary report using the date:
```
    python3.5 <your_repo_location>/reporter.py -n *2017-12-14*
``` 

##### This is the usage of reporter.py	
```
reporter.py [-h] [-n [NAME]]

optional arguments:
  -h, --help            show this help message and exit
  -n [NAME], --name [NAME]
                        filter json file by name
```
