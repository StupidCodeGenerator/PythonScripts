import sqlite3
import os

# Get the profit data from the handActions table
# The result will be a 1D data set.
def GetPlayerDataSet(dbpath):
	connection = sqlite3.connect(dbpath)
	connection.text_factory = str
	c = connection.cursor()
	try:
		c.execute("SELECT Actions.Amount, HandHistory.HandID  FROM Actions \
		CROSS JOIN HandHistory \
		WHERE Actions.HandID = HandHistory.HandID \
		AND PlayerName = 'NiteTrai' AND ActionType != 'ADD' AND GameLimit = '$1-$2'")
	except:
		pass
	
	strList = [];
	amount = 0
	for row in c:
		amount += row[0]
		print("%s, %s\n" % (amount, row[1]))
		strList.append("%s, %s\n" % (amount, row[1]))
	
	file_object = open('result.csv', 'w')
	file_object.writelines(strList)
		
strList = (os.getcwd(), 'HandDatas.sqlite')
dataPath = "/".join(strList)
GetPlayerDataSet(dataPath)