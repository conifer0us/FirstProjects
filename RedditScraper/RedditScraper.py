import praw
from psaw import PushshiftAPI
from praw.models import Submission, MoreComments
from praw.models.comment_forest import CommentForest
import json

class RedditScraper:
    USER_AGENT="Mozilla/5.0 (X11; Linux i686; rv:105.0) Gecko/20100101 Firefox/105.0"
    RESTRICTED_CHARACTERS = '"^#\'\\\n~`*[]'
    SCRAPED_DB = "data.txt"

    def __init__(self, authFile : str) -> None:
        with open(authFile, "r") as authFile:
            authJSON = json.load(authFile)["reddit"]
            self.reddit= praw.Reddit(
                client_id=authJSON["client_id"],
                client_secret=authJSON["client_secret"],
                user_agent=self.USER_AGENT
            )

    def getPosts(self, subreddit : str, num : int):
        PSapi = PushshiftAPI()
        gen = PSapi.search_submissions(subreddit=subreddit, sort="desc", sort_type="score")
        submissionList = []
        for submission in gen:
            if len(submissionList) >= num:
                break
            submissionList.append(submission.id)
        return submissionList
    
    def getCallResponseFromPost(self, postID : str):
        postData = Submission(self.reddit, postID)
        if postData.score < 20: 
            return
        postText = postData.title + " " + postData.selftext
        if postText == " ":
            return
        postData.comment_limit = 50
        postComments = postData.comments
        if len(postComments) == 0:
            return
        if not postData.author:
            authorName = "removed"
        else:
            authorName = postData.author.name
        self.writeDatatoDB(authorName, postText, postComments[0].body)
        self.getCallResponseFromCommentForest(postComments)
        return

    def getCallResponseFromCommentForest(self, commentForest : CommentForest):
        call_comment_list = [comment for comment in commentForest if not isinstance(comment, MoreComments) and comment.score > 4 and comment.author]
        for comment in call_comment_list:
            commentReplies = [reply for reply in comment.replies if not isinstance(reply, MoreComments)]
            if len(commentReplies) > 0 and commentReplies[0].score > 4:
                self.writeDatatoDB(comment.author.name, comment.body, commentReplies[0].body)
                self.getCallResponseFromCommentForest(commentReplies)

    def writeDatatoDB(self, poster : str, call : str, resp : str):
        # print("Data Written:{}\n\n".format(self.formatData(poster, call, resp)))
        with open(self.SCRAPED_DB, "a") as db:
            db.write(self.formatData(poster, call, resp))

    def formatData(self, poster : str, call : str, response : str):
        return "\"" + poster + "\",\"" + self._sanitizeData(call) + "\",\"" + self._sanitizeData(response) + "\"\n"

    def _sanitizeData(self, data : str) -> str:
        for char in self.RESTRICTED_CHARACTERS:
            data = data.replace(char, "")
        return data
