## Description
Final project of SI507 Intermediate programming. This is an application that can visualization overal distribution of review score of movies by combining data from RottenTomatoes and Metacritic.

## Packages prerequist
```
flask, plotly, pandas, collections, nltk, re, selenium, webdriver_manager
```

## For running the program
This application caches raw data in directory `/cache` so you need to create a directly named `cache` in the root directly. After that, just run 
```
python3 main.py
```
Interate with the program on `http://127.0.0.1:5000` by default.

## Data structure
The raw data of reviews are stored in one list of format:
`[[critics reviews], [audience reviews]]`,
where one review is in format: `[reviewer name, time, score, text]`

Example:
```
data = [
    [   
        ["John Smith", "Mar 1, 2023", 0.7, "This is just a review!"], # critics reviews
        ...
    ],
    [
        ["Bot", "Mar 1, 2023", 0.7, "This is just a review!"], # audience review
        ...
    ]
]
```

There’re two trees used: scoreTree and timeTree.
The scoreTree is used for score distribution visualization, and the timeTree is used for visualization of average score with respect to time.

The scoreTree and timeTree are 2-level trees in format:
```
scoreTree = [
    [   # critic reviews
        [review1_index, review2_index, ...], # score 0~1
        [...],  # score 1~2
        ...
    ],
    [   # audience reviews in same format
        [...],
        ...
    ]
]

timeTree = {
    "year" : [
        [review1_score, review2_score, ...], # January
        [...], # February
        ...
    ],
    ...
}
```
The entry in scoreTree are index into raw data, where the entry in timeTree are scores of review.
