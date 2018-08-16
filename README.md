# Visa Journey Data Analysis

Gather data about users' visa statuses at Visa Journey to analyse.

## Important

This repository is only educational, any use of it that goes against Visa Journey's Terms of Use is your own responsability

## How to Run

Edit the `visajourney_scrapy.py` file and change the Country (Set Country as "All" to Download the information for all the countries). Then run the following:

> `brazil_k1.csv` is the name of the file where the data will be output to

```
pipenv install
pipenv run scrapy runspider visajourney_scrapy.py -o brazil_k1.csv
```
