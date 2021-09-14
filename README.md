# Writing Tests

Today we will be writing code and generating tests for that code.

Python is a powerful language, you can do a lot of stuff with it.

# Exercises

## Testing The Basics

In this repo you will find a sqlite database file.  You will need to write the following tests for it, and then set up a CI/CD pipeline for those tests.

* File exists test
* database connection works
* columns exist in table
* Do the 'cleaning the data' exercise before continuing on
* how many nulls per column in each table? 
* how many zeroes per column in each table?
* Do we have all necessary unique values per column per table?
* Do primary keys agree? - do all the primary and foreign keys match up across two tables?

## Cleaning the Data

You will notice, if you inspect the data that the data is very messy - there are multiple values for the notion of "null" for instance.

* create a function for a consistent null value across all tables and columns
* write a test for your function
* add it to your CI/CD pipeline
* run your function over the database and confirm it works
* write a test to ensure this doesn't happen in the future