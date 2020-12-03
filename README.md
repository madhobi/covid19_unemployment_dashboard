# Economic Repurcussions of the COVID-19 Pandemic
This repository contains current economic data, COVID-19 metrics, and a python source file for data visualization. 

The data used in our visualization are contained in the following files:

* COVIDByCountySize.csv
* countyPopSize.csv
* IndustryByState.csv
* IndustryByUS.csv
* LaborForceByCounty.csv
* UnemploymentByCounty.csv


## COVID-19 Cases By County (Per Month)

The file labeled "COVIDByCountyPerMonth.csv" contains information pertaining to COVID-19 cases.

This information has the breakdown of COVID-19 cases per month, starting in January. Each row represents a county and contains four columns describing 
the county name, the county FIPS, the state each county is located in, and the corresponding state FIPS. Every other column is labeled with a month name
corresponding to the number of new cases within that month.

Data source by [USAFacts](https://static.usafacts.org/public/data/covid-19/covid_confirmed_usafacts.csv?_ga=2.181204647.1894161905.1606516527-1693970899.1605913515 "USAFacts COVID-19 Data").


## County Population Size

The file labeled "countyPopSize.csv" contains information pertaining to the overall county population sizes. 

This information has the value for each county size. Each row represents a county and contains four columns describing the county name, the county FIPS, the state each county is located in, and the corresponding state FIPS. The last column contains the county population size.

Data source by [USAFacts](https://static.usafacts.org/public/data/covid-19/covid_county_population_usafacts.csv "USAFacts County Population Size").


## COVID-19 Cases Normalized By County Size (Per Month)

The file labeled "COVIDByCountySize.csv" contains information pertaining to

This information has the breakdown of proportional COVID-19 cases to population size each month, starting in January. Each row represents a county and contains four columns describing the county name, the county FIPS, the state each county is located in, and the corresponding state FIPS. Every other column is labeled with a month name
corresponding to the number of new cases within that month divided by the county size.

Data source by [USAFacts](https://usafacts.org/visualizations/coronavirus-covid-19-spread-map/ "USAFacts COVID-19 Normalized Data").


## Industry Income By State

The file labeled "IndustryByState.csv" contains information pertaining to the income of each industry at the state level. 

This information is a quarterly report of each industry's income based on every state. Each row represents some economic data being represented within a particular state and contains four columns describing the state FIPS (GeoFips), the state name (GeoName), the code given by the BEA to represent each variable (LineCode), and the Description for the LineCode. The first series of columns are labeled by Year:Quarter (ex. 2018:Q1) and represent the currency value. The second series of columns are labeled by \[Year\]\[Quarter\]Change and represent the difference in the last quarter compared to the current quarter.

Data source by [link](http://example.com "Title").


## National Industry Income

The file labeled "IndustryByUS.csv" contains information pertaining to the income of each industry at the national level. 

This information is a quarterly report of each industry's income based on the national summary. Each row represents some economic data being represented at the national level and contains four columns describing: 1) the FIPS (GeoFips), 2) the United States (GeoName), 3) the code given by the BEA to represent each variable (LineCode), and 4) the Description for the LineCode. *Note that the first two will remain the same values, as this dataset summarizes information at the national level.* The first series of columns are labeled by Year:Quarter (ex. 2018:Q1) and represent the currency value. The second series of columns are labeled by \[Year\]\[Quarter\]Change and represent the difference in the last quarter compared to the current quarter.

Data source by [link](http://example.com "Title").


## Unemployment Rates By County 

The file labeled "UnemploymentByCounty.csv" contains information pertaining to
 
Data source by [BLS.GOV](https://www.bls.gov/web/metro/laucntycur14.txt "Employment by County").


## Labor Force By County 

The file labeled "LaborForceByCounty.csv" contains information pertaining to the Civilian Labor Force.

This information has the breakdown of individuals that are eligible to work within each county over the course of several months, starting in January. Each row represents a county and contains four columns describing the county name, the county FIPS, the state each county is located in, and the corresponding state FIPS. Every other column is labeled with a month name corresponding to the number of eligible working individuals. 

**Note that this includes both unemployed and employed individuals.**

In order to get the count of unemployed individuals, take the unemployed rate by county (represented as a percentage), and multiply by the labor force that month.

Data source by [BLS.GOV](https://www.bls.gov/web/metro/laucntycur14.txt "Employment by County").

