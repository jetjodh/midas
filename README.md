# midas

* data_explore.ipynb contains data exploration process undertaken
* scraping.ipynb contains final code used for scraping data
* training.ipynb contains training steps undertaken along with the preprocessing steps and model construction code.
* app.py contains webapp code
* Validation accuracy achieved: 82.37%.

* Things that failed:
1. Using praw to scrape data- too slow and too less data collected. It is too exhaustive to search for posts and collect data for different flairs.
2. Using random forests, SVMs, XGB trees and other ML classifiers for predicting flair- accuracy was far too less to justify using them for the serving process.
3. Using large tf models, as only small slug sizes are permissible in Heroku.
4. Using large tf models, very low point of diminishing return in terms of accuracy.
