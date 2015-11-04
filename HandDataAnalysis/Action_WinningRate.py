# Y - BB/hands Rate
# X - VPIP

import sqlite3
import os
import time

smallBlind = {'$0.05-$0.10':0.05, '$0.10-$0.20':0.10, \
				'$0.15-$0.30':0.15, '$0.25-$0.50':0.25,\
				'$0.50-$1':0.50, '$1-$2':1}
	

def GetNumOfHands(playerName, connectionCursor):
	try:
		connectionCursor.execute("select count(HandHistory.HandID) from PlayerInfo \
			cross join HandHistory \
			on PlayerInfo.HandID = HandHistory.HandID\
			where PlayerName = '" + playerName + "' \
			and SeatType = '6 Max'")
	except:
		pass
	return connectionCursor.fetchone()[0]
	
def GetNumOfVP_PreFlop(playerName, connectionCursor):
	try:
		connectionCursor.execute("select count(distinct HandHistory.HandID) \
			from Actions cross join HandHistory \
			on Actions.HandID = HandHistory.HandID \
			where Actions.ActionType in ('CALL', 'RAISE', 'RE_RAISE', 'BET', 'UNCALLED_BET') \
			and Actions.Street = 1 \
			and Actions.PlayerName = '" + playerName + "' \
			and SeatType = '6 Max'")
	except:
		pass
	return connectionCursor.fetchone()[0]

def GetNumOfRaise_PreFlop(playerName, connectionCursor):
	try:
		connectionCursor.execute("select count(distinct HandHistory.HandID) \
		from Actions cross join HandHistory \
		on Actions.HandID = HandHistory.HandID \
		where Actions.ActionType in ('Bet', 'RAISE', 'RE_RAISE', 'UN_CALLED_BET') \
		and Actions.Street = 1 \
		and Actions.PlayerName = '" + playerName + "' \
		and SeatType = '6 Max'")
	except:
		pass
	return connectionCursor.fetchone()[0]
	
# Get the profit data from the handActions table
# The result will be a 1D data set.
def GetDataSet(dbpath):
	connection = sqlite3.connect(dbpath)
	connection.text_factory = str
	c = connection.cursor()
	
	# CREATE INDEX
	try:
		c.execute("CREATE INDEX idxHandHistory on HandHistory(SeatType, GameLimit)")
		c.execute("CREATE INDEX idxActions on Actions(ActionType,Street,PlayerName, HandID, Amount)")
		c.execute("CREATE INDEX idxPlayerInfo on PlayerInfo(PlayerName, HandID)")
	except:
		pass
	
	# STEP_1 : find all players, make them into a list.
	print ( "Finding PlayerNames...")
	try:
		c.execute("SELECT distinct PlayerInfo.PlayerName FROM PlayerInfo \
			cross join HandHistory \
			on PlayerInfo.HandID = HandHistory.HandID\
			where HandHistory.SeatType = '6 Max'")
	except:
		pass
	playerList = []
	for row in c:
		playerList.append(row[0])
	print ("STEP_1 : find all players over, len=" + str(len(playerList)))
		
	# STEP_2 : for all the players, get there NumOfHands
	print ("Get their numOfHands")
	playerHandCounts = {}
	for playerName in playerList:
		playerHandCounts[playerName] = GetNumOfHands(playerName, c)
		print("HandsCount of %s : %s" % (playerName, str(playerHandCounts[playerName])))
	print ("STEP_2 : count there hands over")
	
	# STEP_3 : get their preflop in pot
	print ("Get VP")
	playerVP = {}
	for playerName in playerList:
		playerVP[playerName] = GetNumOfVP_PreFlop(playerName, c)
		print("VP of %s : %s" % (playerName, str(playerVP[playerName])))

	# STEP_4 : get there preflop raise
	print ("Get PFR")
	playerPFR = {}
	for playerName in playerList:
		playerPFR[playerName] = GetNumOfRaise_PreFlop(playerName, c)
		print("PFR of %s : %s" % (playerName, str(playerPFR[playerName])))
	
	# STEP_5 : Count their profit
	print ("Count Profit")
	try:
		c.execute("SELECT distinct Actions.Amount, Actions.PlayerName, HandHistory.GameLimit FROM Actions \
		CROSS JOIN HandHistory \
		on Actions.HandID = HandHistory.HandID \
		and ActionType != 'ADD'\
		and SeatType = '6 Max'")
	except:
		pass	
	
	playerProfits = {}
	for row in c:
		playerName = row[1]
		if playerName in playerList:
			amount = row[0]/smallBlind[row[2]]
			if playerName in playerProfits.keys():
				playerProfits[playerName] += amount
			else:
				playerProfits[playerName] = amount
	
	# Remove the blank data
	for playerName in playerList:
		if playerName not in playerProfits.keys():
			print ("Removed blank player : " + playerName)
			playerHandCounts.pop(playerName)
			playerVP.pop(playerName)
			playerPFR.pop(playerName)
		elif playerName not in playerVP.keys():
			print ("Removed blank player : " + playerName)
			playerHandCounts.pop(playerName)
			playerPFR.pop(playerName)
			playerProfits.pop(playerName)
		elif playerName not in playerPFR.keys():
			print ("Removed blank player : " + playerName)
			playerHandCounts.pop(playerName)
			playerVP.pop(playerName)
			playerProfits.pop(playerName)
		elif playerName not in playerHandCounts.keys():
			print ("Removed blank player : " + playerName)
			playerVP.pop(playerName)
			playerPFR.pop(playerName)
			playerProfits.pop(playerName)
	
	# Remove Noise
	for playerName in playerList:
		if playerHandCounts[playerName] < 100:
			print ("Removed Noise Player: " + playerName)
			playerHandCounts.pop(playerName)
			playerVP.pop(playerName)
			playerPFR.pop(playerName)
			playerProfits.pop(playerName)
	
	# OUTPUT
	print ("Writing file")
	strList = [];
	amount = 0
	strList.append("playerName, hands, VP, pfr, profit\n")
	for playerName in playerHandCounts.keys():
		if playerName in playerHandCounts.keys() \
		and playerName in playerVP.keys() \
		and playerName in playerPFR.keys() \
		and playerName in playerProfits.keys():
			strList.append(\
			"%s, %s, %s, %s, %s\n" % \
			(playerName, playerHandCounts[playerName], playerVP[playerName], \
			playerPFR[playerName], playerProfits[playerName]))
	
	file_object = open('vpip_result'+str(time.time())+'.csv', 'w')
	file_object.writelines(strList)
		
strList = (os.getcwd(), 'HandDatas.sqlite')
dataPath = "/".join(strList)
GetDataSet(dataPath)