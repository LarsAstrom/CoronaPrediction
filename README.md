# CoronaPrediction
Prediction of number of hospitalised patients in the county of Skåne, Sweden.

## Theory
The underlying theory can be read in the document CoronaPrediction/releases/pdf/rapport_v2.0.pdf. This document is in Swedish.

## Data sources
The input data used is the number of hospitalised patients and the number of deaths of people with confirmed Coronavirus. These are collected from public sources at https://www.skane.se/digitala-rapporter/lagesbild-covid-19-i-skane/inledning/

## Output from program
The program tests many different parameter setups and evaluated the setups' ability to predict the number of hospitalised patients and the number of deaths according to a loss function. The model with the best fit is then returned and used to predict the future.

## Usages of the program
The program's results are delievered daily to Region Skåne, in order for them to use the results, if they want to, for predictions of the future number of hospitalised patients. This can be used to manage the workforce and material supply.

## How to run the program
1. Make sure the input-file CoronaPrediction/input_data/input.csv is up to date.
2. Run the program CoronaPrediction/corona_parameter_timeseries.py using python3.
3. When the program is run, the best parameter setup is logged in CoronaPrediction/log_parameter_tidsserie.csv. The next time the program is run the program will only read in the log-file. If one wants to run the program from scratch, one needs to delete the log-file.
4. Open the excel-file CoronaPrediction/excel_ark/simulation_bugfix.xlsx. 
4a. Make sure the data under the sheet "Data" is up to date.
4b. Enter the parameters given by step 2 in the sheet "Konfiguration".
4c. Now the predictions are available in the sheet "Konfiguration".
