# Mifit analyzer

This tool analyzes the data received from the Mi Band fitness bracelet and generates a report based on it.

Work on this project is still in progress. Not all planned functionality has been implemented yet. However, the current version already allows you to quickly generate an `.html` report on your activity and sleep.

If you have any questions, suggestions, wishes, problems or errors, then you can let me know about them using Git Issues or any other feedback.

In case of errors, send logs from `mifit_analyzer/results/logs/logs.log` file and an error message from the command line so that you can get a faster and better response

Future plans:
* Add module to unzip input archives using passwords
* Add option to use different time zones changed because of travel or movement to other cities/countries
* Add tests
* Add docker
* Add more than 10 different other improvements not mentioned above from my personal plan for this project.

Stay connected. See you soon!

## Installation

### Clone repository

```
$ git clone https://github.com/MVFofanov/mifit_analyzer.git
```

### Move to project directory

```
$ cd mifit_analyzer
```

### Set up virtual environment in working directory via `conda`
* Install Miniconda
```
mkdir -p ~/miniconda3
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O ~/miniconda3/miniconda.sh
bash ~/miniconda3/miniconda.sh -b -u -p ~/miniconda3
rm -rf ~/miniconda3/miniconda.sh
~/miniconda3/bin/conda init bash
```
* Create virtual environment `<env_name>`
```
$ conda create --name <env_name> python=3.10
```
* Activate your new virtual environment `<env_name>`
```
$ conda activate <env_name>
```
* Install some dependencies
```
$ conda install -c conda-forge pympler, pandas, seaborn, pandoc
```

## How to get data from your Xiaomi Mi Band fitness bracelet

* Open the Mi Fit app on your smartphone
* Click the `Profile` button at the bottom right of the screen
* Click the `Settings` button
* Click the `About the app` button
* Click the `User rights` button
* Click the `Data export` button
* Select all data types available for download
* Select the date range you are interested in. The app limits you to a maximum range of 500 days to download at a time. If you wear a bracelet for more than 500 days, then download the data in several approaches.
* Enter your email and verification code
* Receive an email with a data archive and a password for this archive
* Extract the archive using the password to the `mifit_analyzer/data` directory inside the project directory
* Now you are ready for data analysis!

## Usage
```
usage: python3 mifit_analyzer/src/mifit_analyzer/mifit_analyzer.py [options]

options:
  -h, --help            show this help message and exit
  --input_directory INPUT_DIRECTORY
                        path to input directory. Default: mifit_analyzer/data
  --start_date START_DATE
                        start date. Default: 1900.01.01
  --end_date END_DATE   end date. Default: 2100.01.01
  --time_zone TIME_ZONE
                        time zone. Default: 0
  --output_directory OUTPUT_DIRECTORY
                        path to output directory. Default: mifit_analyzer/results
  --daily_steps_goal DAILY_STEPS_GOAL
                        daily steps goal. Default: 8000
  --user_name USER_NAME
                        user name. Default: Username
  --top_step_days_number TOP_STEP_DAYS_NUMBER
                        top step days number. Default: 10
  --date_format DATE_FORMAT
                        date format. Default: YYYY.mm.dd
  --log_mode LOG_MODE   log mode. Default: w

```

## Results

The results of the analysis of your data by this tool are by default in the directory `mifit_analyzer/results`
you can store the results somewhere else using the appropriate option `--output_directory`

The result directory contains several subdirectories:
* `logs`
* `plots`
* `report`
* `statistics` 

The main result of the work of this tool is the HTML file located at the following address: `mifit_analyzer/results/report/report.html`
You can open it in any browser from your computer or mobile phone

This `report.html` file contains all the necessary information regarding the analysis of your data. Explore it yourself, share with friends and have fun!

## Software Requirements

* Python 3.10
* Ubuntu 20.04
* Git 2.25.1
* Bash