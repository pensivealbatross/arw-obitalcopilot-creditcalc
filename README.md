# arw-obitalcopilot-creditcalc
Combines data sources to determine how many credits have been used on Orbital Copilot.

# Requires, setup and run

## Python3
Download and install a current version of [Python3](https://www.python.org/downloads/).

## Required packages
Install required packages with
```
pip install -r requirements.txt
```

## Run
Start the api with
```
./run.sh
```

Then find the api at `http://127.0.0.1:5000/usage` with a browser or with 
```
curl http://127.0.0.1:5000/usage
```

# Thoughts and decisions
I broke the code into three modules with distinct roles. This makes development and testing easier and makes the code more portable should functionality need to be reused somewhere else.
* [creditcalc.py](creditcalc.py) - Main module, deals with creating the server and taking requests on `/usage`
* [orbitalcopilot.py](orbitalcopilot.py) - This module is dedicated to gracefully using the Orbital Copilot APIs
* [calculatecost.py](calculatecost.py) - Dedicated to calculating the cost based on a message. This could have been in the main module, but it needed a lot of testing and it feels like it may be subject to change.

I noticed that the rules around base cost, unique word bonus and palindromes could be interpreted in a number of ways. I decided that the base cost was the start cost AND the minimum cost. And that the minimum should be checked before it might get doubled. Other interpretations would be just as valid so this is worth a check.

## Acuracy
Logging and testing help with accuracy, but as things change, they are no guarenty. Ultimately when accuracy is critical it needs additional consideration. A quality Service Level Objective is a great way to measure accuracy to a well-understood target. A new service may be required to regularly inspect the quality of results and generate the indicator.

# Consessions and left to do
* The log level should be set from the environment.
* The service should be creating custom oTel metrics counting runs and performance statistics.
* Python really messes up basic maths and ends up with loads of decimal places that shouldn't be there. I've used rounding to solve this, but some more thought on that and a better approach would be good.
* The tests in the test functions were useful for developing. But they should be formalised to proper unit tests and expanded.

