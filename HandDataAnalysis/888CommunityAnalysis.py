import sqlite3
import os

# Get the profit data from the handActions table
# The result will be a 1D data set.
def GetPlayerDataSet(dbpath):
	connection = sqlite3.connect(dbpath)
	connection.text_factory = str
	c = connection.cursor()
	try:
		c.execute("select CommunityCards from HandHistory")
	except:
		pass
	
	numOfAce = 0
	numOfAll = 0;
	for row in c:
		if len(row[0]) == 10:
			numOfAll += 1
			rowList = list(row[0])
			if rowList[0] == 'A' or rowList[2] == 'A' or rowList[4] == 'A' \
				or rowList[6] == 'A' or rowList[8] == 'A':
				numOfAce += 1
			
	print ("finalResult : " + str(numOfAce) + "/" + str(numOfAll))
			
strList = (os.getcwd(), 'HandDatas.sqlite')
dataPath = "/".join(strList)
GetPlayerDataSet(dataPath)