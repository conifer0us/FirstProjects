# Reddit Scraper

Some python code to mine a set of comment/reply pairs off of a certain set of subreddits. I'm not sure it would work now (or how expensive it would be) with reddit API changes, but before the crackdown it got about 700mb of text data from about 10 subreddits over a few hours. Certainly not the best.

The data is still out there, but it's too big to just throw in the repo. It could definitely be used to train a language model, but it would be horrible to talk to. If I ever do that, the data will be public with it.

If anyone ever does run the code, there should be an auth.json file with the reddit API auth information in it. The data is put out to data.txt
