# SI507-Final-Project
repository for SI507 Final Project

## Introduction

The purpose of this project is to build a basic web application via Flask, about the most recent bird observations around the US by states (DC, Puerto Rico, Guam and other U.S. territory are not included; 50 state altogether). Users can type a state's name to see 10 most recent bird species ranging from 2020/11/04 - 2020/12/14. Then, based on the results, users can either back to the home page to explore a new state, or continue to get descriptions about the bird species that they are interested in.

## Data Sources
[ebird API documentation](https://documenter.getpostman.com/view/664302/S1ENwy59?version=latest)
API that contains most recent bird observations for all bird species around the world. For this project, we just restrict the region to the US.
API key is required. Get a key by registration.

[ebird offical website](https://ebird.org/explore)
A website that contains information of all bird species.

## Usage
### Step 1: get an key for eBird api
Go to the documentation page, click "sign up" to sign up an account and get an API key.
Make your key secret. If you want to run my program, my key is provided in the final submission document (no sensitive info involved).

### Step 2: Install all the required packages: requests, flask, sqlite3 (pip or pip3) as the example below
```bash
pip3 install flask
```
### Step 3: Open si507_flask.py
Please make sure to change the path of the database file when running on your own laptop

### Step 4: Open "http://127.0.0.1:5000/" in a browser and enjoy!
