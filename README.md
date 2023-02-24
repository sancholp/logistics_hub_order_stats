# Logistics hub order exploration

In this project I explore a dataset on the orders placed during the month of August at a logistics hub of an online supermarket. 

The dataset, located in `data/orders.csv`, consists of two columns of timestamps, one for when an order was placed, and one for when it was delivered.

In `data_exploration.ipynb` I explore the dataset, analyzing some statistics and drawing conclusions. 

In `script/` there's a Python script that detects any abnormal store closures, as well as a simple model to estimate the number of missed orders during these closures. The script is executed by running `main.py`. Chapter 3 of `data_exploration.ipynb` gives a brief explanation of the thought process behind this script. 
