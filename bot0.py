# script runs CheerB0t to check all comments on reddit (besides blacklisted subreddits)
import praw
import json
import nltk
import random

def botLogin():
	bot = praw.Reddit(client_id='CTiJ3GSR0H4oHg',
		client_secret='-U3YrdWAcoNfYKBMIPeowDzDbmc',
		user_agent='cheerb0t',
		username='cheerb0t',
		password='')
	return bot

def getImg(bot):
        funsub = bot.subreddit('wholesomecomics')
        posts = funsub.top(limit=60)
        ranNum = random.randint(0,59)
        for i,post in enumerate(posts):
                if i==ranNum:
                        return post.url

def getMsg():
        msgNum = random.randint(0,8)
        if msgNum == 0:
                message = " [Maybe this will cheer you up?]("
        elif msgNum == 1:
                message = " [Maybe this comic will cheer you?]("
        elif msgNum == 2:
                message = " [Here's something to cheer you up.]("
        elif msgNum == 3:
                message = " [Here's a comic for you.]("
        elif msgNum == 4:
                message = " [Maybe this can brighten your day.]("
        elif msgNum == 5:
                message = " [Maybe this can lighten the mood.]("
        elif msgNum == 6:
                message = " [Maybe this can make you feel better.]("
        elif msgNum == 7:
                message = " [Hopefully this cheers you up.]("
        else:
                message = " [Maybe this will cheer you up?]("
        return message

bot = botLogin()

file = open("stress.json");
reader = file.read()
data = json.loads(reader)

subreddit = bot.subreddit('all')

blacklist = {'askreddit','funny','gaming','news','the_donald','dankmemes','television',
             'globaloffensive','2007scape','pathofexile','warframe','nfl','overwatch',
             'gameofthrones','anime','comicbooks','starwars','pubattlegrounds','games',
             'prequelmemes','warframe','hearthstone','4chan','rainbow6','starwarsbattlefront',
             'leagueoflegends','magictcg','greenday','copypasta','buffalobills','offmychest',
             'wrestlingisreddit'}

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
        if token in data and token not in wordList:
            totScore += int(data[token])
            wordList.append(token)
            wordList.append(data[token])
    comp = float(totScore)/float(totWords)
    if totScore < -22 and comp < -0.17:
            message = "{0}, your post indicated a high level of stress.\n".format(comment.author)
            message += getMsg()
            message += getImg(bot)+")\n\n ^-automated ^message ^by ^bot"
            comment.reply(message)
            print ('Commented in ',comment.subreddit)
            # print '\n TESTER:'
            # print comment.subreddit
            # print comment.author
            # print comment.body
            print wordList
            print totScore
            print comp
            # print message
            
