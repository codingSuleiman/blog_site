import csv

dataBase = {}
dataFile = open('EmployeeData.csv', encoding = "ISO-8859-1")
dataOrg = csv.reader(dataFile)
employee_name = ''

for data in dataOrg:
	dataBase[data[0]] = [data[i] for i in range(1,14)]

def accessDatabase(userId):
	dataInfo = ''	
	for dataKey in dataBase.keys():
		if dataKey == userId.upper():
			dataInfo = dataBase[dataKey]
			
	sampleHeader = dataBase[next(iter(dataBase))]
	return zip(sampleHeader,dataInfo)

