# Find out what are the most valueable holeCard

import sqlite3
import os
import time

def HoleCardsConvert(holeCardStr):
	charList = list(holeCardStr)
	result = charList[0] + charList[3]
	if charList[1] == charList[4]:
		result += 's'
	else: 
		result += 'o'
	return result

def GetPlayerDataSet(dbpath):
	connection = sqlite3.connect(dbpath)
	connection.text_factory = str
	c = connection.cursor()
	
	print ("Searching Data...")
	try:
		c.execute("select HoleCards, Amount from PlayerInfo cross join Actions \
			on Actions.HandID = PlayerInfo.HandID \
			where HoleCards != 'NULL' and Amount > 0")
	except:
		pass
		
	print ("Calculating result...")
	resultDic = {}
	for row in c:
		print(row)
		cardType = HoleCardsConvert(row[0])
		if cardType in resultDic.keys():
			resultDic[cardType] += row[1]
		else:
			resultDic[cardType] = row[1]
	
	strList = []
	for (k,v) in  resultDic.items():
		strList.append("%s,%s\n" % (k,v))

	file_object = open('CardRate'+str(time.time())+'.csv', 'w')
	file_object.writelines(strList)
			
strList = (os.getcwd(), 'HandDatas.sqlite')
dataPath = "/".join(strList)
GetPlayerDataSet(dataPath)