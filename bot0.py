# script runs CheerB0t to check all comments on reddit (besides blacklisted subreddits)
import praw
import json
import nltk
import random

def bot_login():
	bot = praw.Reddit(client_id='CTiJ3GSR0H4oHg',
		client_secret='-U3YrdWAcoNfYKBMIPeowDzDbmc',
		user_agent='cheerb0t',
		username='cheerb0t',
		password='')
	return bot

def getImage(bot):
        funsub = bot.subreddit('wholesomecomics')
        posts = funsub.top(limit=60)
        ranNum = random.randint(0,59)
        for i,post in enumerate(posts):
                if i==ranNum:
                        return post.url

bot = bot_login()

file = open("afinn.json");
reader = file.read()
data = json.loads(reader)

subreddit = bot.subreddit('all')

blacklist = {'askreddit','funny'}

comments = subreddit.stream.comments()

for comment in comments:
    if comment.subreddit.display_name.lower() in blacklist:
            continue 
    wordList = []
    totScore = 0
    totWords = 0
    comp = 0
    str = (comment.body).lower()
    totWords = len(str.split())
    tokens = nltk.word_tokenize(str)
    # print submission.title, ' >>>  ', totWords
    for token in tokens:
        if token in data:
            totScore += int(data[token])
            wordList.append(token)
            wordList.append(data[token])
    # print wordList
    # print totScore
    comp = float(totScore)/float(totWords)
    # print('Comparitive: ',comp)
    if totScore < -25 and comp < -0.25:
            funImg = getImage(bot)
            message = "{0}, your post indicated a high level of stress.\n".format(comment.author)
            message += " [Maybe this will cheer you up?]("+funImg+")"
            message += "\n\n\n\n ^-automated ^message ^by ^bot"
            comment.reply(message)
            print message
            
            
