## Indy Python wrapper test

This is a Python wrapper test for Indy. The tests are not driven by any unit test framework but are standalone python scripts.
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
          - check_connection.py
          - keyrings_wallets.py 
          - remove_and_add_role.py 
          - special_case_trust_anchor_role.py 
          - verify_messages_on_connection.py
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
     
- test_runner.py: The test runner does all the work to run all test scripts, track time, kill dead tests. You are able to specify the directory and run all scripts in the sub directories as well as run all tests (master run) or a limited number of tests by specifying a single sub directory.

- reporter.py: Generate an HTML report to show the summary all the tests run during the same timeframe (example: all test run on 2017-11-16 would be in one report with that date). This would include tests that were run multiple times in a single day. And the report is stored in the 'reporter summary report' folder.
- reporter_summary_report: Containing the html report. (Will be generated after first run).
- test_output:  Will be generated after first run.
     - log_files: Containing the log files of each failed test case.
     - test_results: Containing the json result files of test case.

### How to run

After building successfully the Indy SDK for Python, you need to run the commands below so that could run the tests:

- Install base58 dependency with pip install: 
```
     python3.5 -m pip install base58
```
- Setup PYTHONPATH: 
```
    export PYTHONPATH=$PYTHONPATH:your_repo_location/Automation-Tests
```

#### Then run:
- Run one test case:
```
    python3.5 Automation-Tests/test_scripts/functional_tests/wallet/open_wallet.py
```
- Run a folder test case using test_runner.py:
```
    python3.5 Automation-Tests/test_runner.py -d Automation-Tests/test_scripts/functional_tests/wallet
```
- Run all test cases in the project using test_runner.py:
```    
    python3.5 Automation-Tests/test_runner.py -rd
```
##### This is the usage of test_runner.py
```
test_runner.py [-h] [-d [DIRECTORY]] [-rd [RECUR_DIRECTORY]]
                      [-t [TIMEOUT]] [-html] [-l]

optional arguments:
  -h, --help            show this help message and exit
  -d [DIRECTORY], --directory [DIRECTORY]
                        directory of test scenarios (not recursive)
  -rd [RECUR_DIRECTORY], --recur_directory [RECUR_DIRECTORY]
                        directory of test scenarios (recursive)
  -t [TIMEOUT], --timeout [TIMEOUT]
                        timeout for each scenario (default: 300s)
  -html, --html_report  if this flag is missing, html report would not be
                        generated
  -l, --keep_log        keep all log file
```
#### Generate the html report:
- Get the summary report for all the run
```
    python3.5 your_repo_location/functional_tests/reporter.py
```
- Get the summary report for a group of test cases.
```
    python3.5 Automation-Tests/reporter.py -n *wallet*
```
- Get the summary report using the date
```
    python3.5 Automation-Tests/reporter.py -n *2017-12-14*
``` 

##### This is the usage of reporter.py
```
reporter.py [-h] [-n [NAME]]

optional arguments:
  -h, --help            show this help message and exit
  -n [NAME], --name [NAME]
                        filter json file by name
```
