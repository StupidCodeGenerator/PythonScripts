#FOLD,
#CALL,
#CHECK,
#ANTE,
#SHOW,
#SHOWS_FOR_LOW,
#WINS,
#WINS_THE_LOW,
#WINS_SIDE_POT,
#DEALT_HERO_CARDS,
#TIES,
#TIES_SIDE_POT,
#RAISE,
#RE_RAISE,
#BET,
#SMALL_BLIND,
#BIG_BLIND,
#UNCALLED_BET,
#REQUEST_TIME,
#FIFTEEN_SECONDS_LEFT,
#FIVE_SECONDS_LEFT,
#MUCKS,
#POSTS,
#DISCONNECTED,
#RECONNECTED,
#STANDS_UP,
#SITS_DOWN,
#SITTING_OUT,
#ERROR,
#ADDS,
#TIMED_OUT,
#RETURNED,
#SECONDS_TO_RECONNECT,
#CHAT,
#FEELING_CHANGE,
#ALL_IN,
#GAME_CANCELLED,
#RABBIT,
#UNKNOWN

import sqlite3
import os

# Get the profit data from the handActions table
# The result will be a 1D data set.
# ActionType: Raise = 12, ReRaise = 13, Bet = 14
def GetPlayerDataSet(dbpath):
	connection = sqlite3.connect(dbpath)
	connection.text_factory = str
	c = connection.cursor()
	try:
		c.execute("select * from PlayerInfo where HoleCards in ('As#Ks', 'Ad#Kd', 'Ah#Kh', 'Ac#Kc')")  # AKs
	except:
		pass
		
	cardTypeDict = {}
	for row in c:
		if row[1] != 'NULL' :
			print(row)
	
	print("########################################")
	
	try:
		c.execute("SELECT HandID,ActionType,Amount FROM Actions WHERE PlayerName = 'Answer_42' AND Street = 1")
	except:
		print("sql error")
	
	actionDict = {}

	for row in c:
		if row[2] <= 0:
			if row[0] in actionDict.keys():
				actionDict[row[0]] +=(-row[2])
			else:
				actionDict[row[0]] = (-row[2])
				
	for row in actionDict:
		if row in cardTypeDict.keys():
			print(",".join([cardTypeDict[row], str(actionDict[row])]))
				
strList = (os.getcwd(), 'HandDatas.sqlite')
dataPath = "/".join(strList)
GetPlayerDataSet(dataPath)