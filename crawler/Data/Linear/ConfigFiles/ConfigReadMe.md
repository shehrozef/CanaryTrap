# ConfigVariables

## Config Linear:

* `FB_USER`: email address of the facebook account used for the experiment
* `FB_PASS`: password of the facebook account used for the experiment
* `FIREFOX_PROFILE_PATH`: `/path/to/default/firefox/profile`
* `GEKODRIVER_PATH`: `/path/to/geckodriver`
* `EMAIL_DOMAIN`: domain of the email server used for monitoring emails
* `EMAIL_RECEIPIENT`: email address for monitoring experiment crashes. This is where a failed email is sent.

* `DEPLOYMENT_TYPE`: Path/to/the/folder/of/data/
* `EXPERIMENT_TYPE`: Weather the experiment is linear or array (details in the paper)
* `APPLICATIONS_FILE`: Name of file used to fetch apps for processing
* `URL_START`: Start integer of apps to be processed
* `URL_END`: End integer of apps to be processed
* `HEADLESS`: false 
* `RESULTS`: Name of csv files to store the results of succesfully processed apps
* `PROCESSED_APPS`: Name of csv files to store the apps processed
* `NO_GO`: Apps that are broken so future experiments skip them