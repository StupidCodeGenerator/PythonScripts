# For each numOfBets (1~3), example AA
# Calculate P(RAISE), P(AA), P(RAISE|AA)
# Then calculate P(AA|RAISE)

# Oh preflop first
from __future__ import division
from pymongo import MongoClient

cards = ["A","K","Q","J","T","9","8","7","6","5","4","3","2"]

def GetAllHoleCombinations():
	result = []
	for c1 in cards:
		for c2 in cards:
			holeStr = c1 + c2;
			if(c1 == c2):
				result.append(holeStr);
			else :
				result.append(holeStr + "s");
				result.append(holeStr + "o");
	return result;

client = MongoClient()
db = client.preflop

def CalculationOfBets(numOfBets):
	print("Calculation of "+str(numOfBets)+" raise")
	
	dataFilter = {"numOfBets":numOfBets}
	cursor = db.HandHistories.find(dataFilter);
	
	countS = cursor.count();
	raiseCount = 0
	raiseCountGivenCard = {}
	allCards = GetAllHoleCombinations()
	cardAppearCount = {}
	
	for holeCard in allCards:
		raiseCountGivenCard[holeCard] = 0
		cardAppearCount[holeCard] = 1; # avoid devide by zero
	
	for document in cursor:
		cardAppearCount[document["holeCardShort"]] += 1;
		if(document["actionType"] == "RAISE"):
			raiseCount += 1
			raiseCountGivenCard[document["holeCardShort"]] += 1
	
	fileObject = open("HoleCardPossibilities_"+str(numOfBets)+".txt","w");
	
	pRaise = raiseCount/countS
	fileObject.write("pRaise,pCardAppear,pRaiseGivenCard,bayesResult\r\n")
	for key in allCards:
		pCardAppear = cardAppearCount[key] / countS
		pRaiseGivenCard = raiseCountGivenCard[key] / cardAppearCount[key]
		bayesResult = pRaiseGivenCard * pCardAppear / pRaise
		fileObject.write(str(key)+ "," + str(pRaise) + "," + str(pCardAppear) + "," + \
			str(pRaiseGivenCard) + "," + str(bayesResult) + "\n")

############################################

for i in range(0,3):
	CalculationOfBets(i)
