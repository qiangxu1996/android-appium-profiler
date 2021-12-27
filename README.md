# android-appium-profiler

An energy measurement framework for Android apps based on Appium.

## Setup

```bash
npm install -g appium
conda create -n aap poetry appium-python-client -c conda-forge
conda activate aap
mkdir <work dir> && cd <work dir>
git clone https://github.com/qiangxu1996/android-appium-profiler.git
git clone https://github.com/qiangxu1996/ftrace-energy.git
# Setup ftrace-energy by following its README
```

## Writing automation script for an app

To write an automation sciript for a new app, create a Python file in `android_appium_profiler.apps` submodule. Inside the Python file, implement a class with name `App` and inherits `app_test.AppTest`.

Inherit the function `app_test.AppTest.actions`. Within the function, call `self.may_start_profiler()` and `self.may_stop_profiler()` right before and after the region you want to measure. Use `self.driver` to access Appium functionalities, while `app_test.AppTest` also provides many helper functions.

Multiple example scripts for different apps are provided.

## Running an automation script

First start the appium server:

```bash
export JAVA_HOME=<path to jdk>
export ANDROID_SDK_ROOT=<path to android sdk>
appium --allow-insecure chromedriver_autodownload
```

Then start the script (in another shell):

```bash
python android_appium_profiler/run_test.py -f <app script name, e.g., amaze>
```

The option `-f` measures energy consumption using ftrace based power models. Refer to the source code for other options.

## Generating coverage files

Before running the test, configure and install the [AppiumCoverage](https://github.com/qiangxu1996/AppiumCoverage.git) app. Add `-c coverage.ec` when running `run_test.py`. The coverage file `coverage.ec` will be pulled into your current directory after test.

