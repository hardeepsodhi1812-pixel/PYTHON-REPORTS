# Netflix Movies and TV Shows Analysis

Mini project for **Python Programming (25CAH-221)**, Chandigarh University.

| | |
|---|---|
| **Submitted by** | Hardeep Singh Sodhi |
| **UID** | 25bcd10215 |
| **Class** | 25BCD-2(A) |
| **Submitted to** | Ms. Preeti Verma |

## About the project

This project performs an Exploratory Data Analysis (EDA) on the Netflix Movies and TV Shows dataset. It focuses on three things:

- **Genres**: which genres are most common, for movies and TV shows separately
- **Ratings**: how content ratings (TV-MA, TV-14, PG-13, etc.) and audience groups are distributed
- **Release years**: how the number of titles changes by release year and decade

Libraries used: **Pandas, NumPy, Matplotlib, Seaborn**.

## Dataset

- File: `netflix_titles.csv` (7,787 rows, 12 columns)
- Source: Shivam Bansal, *Netflix Movies and TV Shows*, Kaggle
  https://www.kaggle.com/datasets/shivamb/netflix-shows
- Columns: `show_id, type, title, director, cast, country, date_added, release_year, rating, duration, listed_in, description`

## Files

```
.
├── netflix_analysis.py                 # complete analysis code
├── netflix_titles.csv                  # dataset (download separately, see above)
├── Netflix_Analysis_Mini_Project.pdf   # project report
└── README.md
```

Running the script also creates 10 chart images (`f1_type.png` to `f10_added.png`) and a `stats.json` file with the computed numbers.

## Requirements

- Python 3.8 or later
- pandas, numpy, matplotlib, seaborn

Install them with:

```bash
pip install pandas numpy matplotlib seaborn
```

## How to run

1. Download `netflix_titles.csv` from Kaggle and place it in the same folder as `netflix_analysis.py`.
2. Open a terminal in that folder and run:

```bash
python netflix_analysis.py
```

3. The charts are saved as PNG files in the same folder, and the summary numbers are printed in the terminal.

## What the code does

1. **Loads** the CSV with Pandas.
2. **Cleans** the data: fills missing `rating` and `country` with "Unknown", converts `date_added` to datetime, creates `year_added` and `decade` columns.
3. **Splits genres**: `listed_in` holds several genres in one cell, so it is split and expanded with `explode()`.
4. **Analyses** genres, ratings, release years, movie duration and year added, using NumPy for mean, median, standard deviation and percentiles.
5. **Plots** count plots, bar plots, a line chart, histograms and a heatmap with Seaborn and Matplotlib.

## Key findings

- Movies are about 69% of the catalogue and TV shows about 31%.
- Top genres: International Movies (2,437), Dramas (2,106) and Comedies (1,471).
- TV-MA (2,863) and TV-14 (1,931) are the most common ratings, together about 62% of all titles.
- About 70% of titles were released in 2015 or later, and 2018 is the peak release year (1,121 titles).
- The average movie runs about 99 minutes, and about 67% of TV shows have only one season.

## Note

Genre counts add up to more than the number of titles because one title can belong to more than one genre. The dataset was collected in early 2021, so the last years are incomplete.
