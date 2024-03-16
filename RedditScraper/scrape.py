reddits = ["fifthworldproblems", "seventhworldproblems", "AITA", "AskReddit", "TrueOffMyChest", "Confession", "Confessions", "TellMeAFact", "LifeofNorman", "MaliciousCompliance", "InsaneParents", "CopyPasta", "3amjokes", "ExplainLikeImFive", "IDontWorkHereLady", "DadJokes", "TalesFromTechSupport", "TalesFromRetail", "Glitch_In_The_Matrix", "BritishProblems", "WhoWouldWin", "TraditionalCurses", "WritingPrompts", "TwoSentenceHorror", "NoSleep", "UnresolvedMysteries", "AskHistorians", "TIFU", "TrueAskReddit", "ProRevenge", "ExplianLikeIAmA", "Relationships", "AskScienceFiction"]

from RedditScraper import RedditScraper

redditScraper = RedditScraper("auth.json")
for subreddit in reddits:
    print("Scraping "+subreddit)
    posts = redditScraper.getPosts(subreddit, 10000)
    for post in posts:
        redditScraper.getCallResponseFromPost(post)