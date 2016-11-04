#This file contains the class that will crawl reddit to find spoiler threads, and catalog each comment as a training example for the given show.

#1st task. Be able to read in the first result of a series subreddit, and get first 10 comments.
import praw


#we are using a reddit wrapper API for this.
r = praw.Reddit(user_agent='my_cool_application')

#lets get all the top 5 submissions from a particular series subreddit.
##will have to schedule these calls, to make sure we can maximize throughput.

#also you could call the getAllShows() api function? or just call the SQL database again.
#Which is better practice? We don't have an ORM for our DB so im tempted to say the latter.
submissions = r.get_subreddit('gameofthrones')
#


#print [str(x) for x in submissions]

flat_comments = praw.helpers.flatten_tree(submissions.get_comments())[0:4]

for comment in flat_comments:
    print comment.subreddit, " ",comment.author," ",comment.score," ",comment.body[:50],"\n"
