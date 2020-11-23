# CanaryTrap Code

## Requirements:

- Firefox
- Geckodriver
- Selenium
- Python 3+

This Repository is a setup that runs CanaryTrap's Array (also referred as Linear in the code) framework on Facebook. For this first of all run "requirements.txt" to install all packages.

Before you start the experiment there are some files that you need to produce and some config files that need to be edited.

- Data/Linear/sample_apps.csv currently has 1024 apps and there details. You will be required to update this file keeping the formating intact for your own experiment.

- Data/Linear/ConfigFiles/config_linear.json has all params for running the experiment but requires you to update the first 6 parameters according to your setup.
  * `FB_USER` : Email address of FB account
  * `FB_PASS` : Password of FB account
  * `FIREFOX_PROFILE_PATH` : Path of default firefox profile
  * `GEKODRIVER_PATH` : Path of geckodriver
  * `EMAIL_DOMAIN` : Domain of Honeytokens
  * `EMAIL_RECEIPIENT` : Email at which updates are recieved about the experiment


## Running:

`cd` to location of `ProcessApplications.py` and run `python ProcessApplications.py config_linear.json`

## Monitoring Abuse:

*To be done by the person running CanaryTrap*

To monitor abuse CanaryTrap inspects emails recieved on the `Honeytokens`. For this an email server is needed to be set up that allow accessing emails through SSH and credentials/details of the server will go in config_email_server.json

## Modules:

* `SeleniumFunctions` : For controlling all driver functions
* `UtilityFunctions` : For generic functions such as file reading
* `Facebook` : For actions such as logging in, Installing applications, removing etc
* `Logger` : To log activity
* `ThirdParty` : Specific functions related to applications such as status of app

## Logging:

Detailed logs of the experiment will be generated in "Data/Linear/ActionLog.txt"
