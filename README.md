# midas

* data_explore.ipynb contains data exploration process undertaken
* scraping.ipynb contains final code used for scraping data
* training.ipynb contains training steps undertaken along with the preprocessing steps and model construction code.
* Things that failed:
1. Using praw to scrape data- too slow and too less data collected. It is too exhaustive to search for posts and collect data for different flairs.
2. Using random forests, SVMs, XGB trees and other ML classifiers for predicting flair- accuracy was far too less to jusstify using them for the serving process.
