# METAR_Data

## Business Problem

Dodo Flight School (DFS, made up name) has hired you to help them decide the location for their next expansion. DFS has provided historical weather data for various airports across the United States. The deliverable will consist of the 10 most ideal locations to be considered for expansion.

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

---

## Data Sources:

| Name | Source | Link in Repo
|---| --- | --- |
| METAR | Data file is too large for GitHub, link provided to [Google Drive](https://drive.google.com/file/d/1zWxiJHauokV333yBvHGIm_QeeTsAtb6x/view?usp=drive_link)| [link](./data/metar_export.txt)
| Airports | [Kaggle](https://www.kaggle.com/datasets/aravindram11/list-of-us-airports) | [link](./data/airports.csv)
| Population | [Data.gov](https://catalog.data.gov/dataset/500-cities-city-level-data-gis-friendly-format-2019-release) | [link](./data/us_pop.csv)

___

## Data Cleaning

* US Population
    * Primary column that needed to be cleaned up was the Geolocation, which was a set of coordinates read in as a string. The column was split into latitude and logitude and then converted to floats.
    
* Airports
    * This data file did not require cleaning as it was already in the desired format.
    
* METAR
    * Many of the columns were read in with observations in the wrong column.
    * Regular Expressions were used to parse out numbers from different columns (eg. Wind Speed has speed, direction, and Knots), but only the speed was necessary.
    * The cloud cover column was converted to an ordinal variable with the highest values corresponding to the most desirable condition, Clear.
    * Visibility had similar issues to the wind speed column (number with a corresponding letter).
    
___

## Exploratory Data Analysis