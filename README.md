# PM2.5 Incidence Inequality in Eindhoven

This repo accompanies and supports the report available on the folder Documentation, titled 'PM2.5_Incidence_Inequality_in_Eindhoven' in PDF and .tex format, along with the sources in 'sources.bib'.

All datasets are inside the Datasets folder, which is divided into all individual Air Pollution Datasets, contained in the AirPollutionDatasets, all raw datasets like the merger of all the air pollution datasets, neighbourhoods, green spaces, and other unused datasets.
In the folder, it also containts all the clean datasets for average personal income, green spaces, air pollution and the version of the dataset with predicted values. along with geographical data for the wijkens.

Under the Images folder, the reader can find all images used in the report.

The notebooks folder contains all jupyter notebooks and scripts used during the research process.
The notebook DATA-CLEANING contains the code that cleans the datasets. The notebook EDA contains all Exploratory Data Analysis. It is here that one can find the image comparing the mean values of air pollution against the harmful levels.
The notebook MACHINE-EARNING-THOSE-KPIS contains all research and modelling reported on the Results section of the report (except when it refers to the Exploratory Data Analysis).
The script predicting_air_pollutants creates the .csv file called 'predicted_air_pollution' in Datasets folder. The script script-csvs scrapes all air pollution datasets from the web and creates all the csvs in AirPollutionDatasets folder which is under the Datasets folder.
The script script-merging merges all the csvs in the AirPollutionDatasets folder and 'creates merged_air_pollution_data.csv' in Raw Datasets.

The structure is as follows:
```
EINDHOVENCLIMATEINEQUALITY/
│
├── Datasets/
│   ├── AirPollutionDatasets/
│   │   └── [All scraped air pollution datasets]
│   │
│   ├── Raw Datasets/
│   │   ├── merged_air_pollution_data.csv
│   │   ├── real-time, sensor, green spaces, and other raw data
│   │
│   ├── Average personal income.csv
│   ├── green-spaces.csv
│   ├── merged_air_pollution_data_clean.csv
│   ├── predicted_air_pollution.csv
│   ├── wijkens shapefiles (.shp, .shx, .dbf, etc.)
│
├── Documentation/
│   ├── PM2.5_Incidence_Inequality_in_Eindhoven.pdf
│   ├── PM2.5_Incidence_Inequality_in_Eindhoven.tex
│   ├── [Associated .aux, .log, etc. LaTeX files]
│   └── sources.bib
│
├── Images/
│   └── [All figures used in the report]
│
├── Notebooks/
│   ├── DATA-CLEANING.ipynb  
│   │   └── Code for cleaning all datasets.
│   ├── EDA.ipynb  
│   │   └── Exploratory Data Analysis including comparisons of air pollution against thresholds.
│   ├── MACHINE-EARNING-THOSE-KPIS.ipynb  
│   │   └── Modelling and results (except for EDA).
│   ├── predicting_air_pollutants.py  
│   │   └── Predicts pollution values and outputs `predicted_air_pollution.csv`.
│   ├── script-csvs.py  
│   │   └── Scrapes and stores all air pollution datasets in `AirPollutionDatasets/`.
│   └── script-merging.py  
│       └── Merges all pollution CSVs into `merged_air_pollution_data.csv`.
```

To install all packages needed, run ```pip install -r requirements.txt``` on the console
