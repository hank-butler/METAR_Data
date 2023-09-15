# METAR_Data

## Business Problem

Dodo Flight School (DFS, made up name) has hired you to help them decide the location for their next expansion. DFS has provided historical weather data for various airports across the United States. The deliverable will consist of the 10 most ideal locations to be considered for expansion.

## Data Sources:

| Name | Source
|---| --- |
| METAR | Data file is too large for GitHub, link provided to [Google Drive](https://drive.google.com/file/d/1zWxiJHauokV333yBvHGIm_QeeTsAtb6x/view?usp=drive_link)|
| Airports | [Kaggle](https://www.kaggle.com/datasets/aravindram11/list-of-us-airports)
| Population | [Data.gov](https://catalog.data.gov/dataset/500-cities-city-level-data-gis-friendly-format-2019-release)

___

## Criteria for Expansion:

- Continental US
- Near an airport (obviously)
- Weather is most important factor
- Most flight training is done during day
- General Rule of Thumb for ideal weather:
  - Visiblity of 10 miles or more
  - Cloud Ceiling of 3,000 ft above ground or higher (cloud cover column in dataset)
  - Winds less than 15 kts


## Methodology

1. Cleaning data
  * RegEx
  * Filtering/Imputation
2. Exploratory Data Analysis
3. Clustering Approach
4. Recommendations