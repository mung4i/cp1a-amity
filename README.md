# cp1a-amity
[![Build Status](https://travis-ci.org/mungaiandela/cp1a-amity.svg?branch=develop)](https://travis-ci.org/mungaiandela/cp1a-amity)
[![Coverage Status](https://coveralls.io/repos/github/mungaiandela/cp1a-amity/badge.svg?branch=develop)](https://coveralls.io/github/mungaiandela/cp1a-amity?branch=develop)


## Background
Amity is an Andela facility and this is the system that runs it.
Amity has rooms which can be offices or living spaces.
An office can accommodate a maximum of 6 people.
A living space can accommodate a maximum of 4 people.
A person to be allocated could be a fellow or staff.
Staff cannot be allocated living spaces.
Fellows have a choice to choose a living space or not.
This system will be used to automatically allocate spaces to people at random.

## Set Up
To set up the app on your local machine:

* Create project directory and change into it
    `mkdir cp1a && cd /cp1a `

* If you use virtualenvwrapper
    `mkvirtualenv cp1a-amity`

* If not
    `virtualenv cp1a-amity`
    `source cp1a-amity/bin/activate`

* Git clone this repository

* Pip install requirements.txt
    `pip install -r requirements.txt`

* Run the application
    `python app.py`
