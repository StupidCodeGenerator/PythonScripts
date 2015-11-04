import sqlite3
import os

# Get the profit data from the handActions table
# The result will be a 1D data set.
def GetPlayerDataSet(dbpath):
	connection = sqlite3.connect(dbpath)
	connection.text_factory = str
	c = connection.cursor()
	try:
		c.execute("SELECT Actions.PlayerName, Actions.Amount FROM Actions CROSS JOIN \
			HandHistory WHERE Actions.HandID = HandHistory.HandID AND \
			SeatType = '6 Max' And ActionType != 'ADD' and GameLimit = '$1-$2'")
	except:
		pass
	
	nameAmountDict = {}
	for row in c:
		playerName = row[0]
		amount = row[1]
		if playerName in nameAmountDict.keys():
			nameAmountDict[playerName] += amount
		else:
			nameAmountDict[playerName] = amount
	
	strList = []
	for (k,v) in  nameAmountDict.items():
		if v > 0:
			strList.append("%s,%s\n" % (k,v))
			print ("%s," % k,v)

	file_object = open('result.csv', 'w')
	file_object.writelines(strList)
			
strList = (os.getcwd(), 'HandDatas.sqlite')
dataPath = "/".join(strList)
GetPlayerDataSet(dataPath)