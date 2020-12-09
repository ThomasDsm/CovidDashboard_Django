import json
import requests
import os
import MySQLdb
from datetime import datetime, timedelta
  
#	https://likegeeks.com/downloading-files-using-python/
#	https://stackoverflow.com/questions/12965203/how-to-get-json-from-webpage-into-python-script
#	https://mysqlclient.readthedocs.io/user_guide.html
#	https://stackoverflow.com/questions/441147/how-to-subtract-a-day-from-a-date

# JSON date not older than 2 day is not accurate and can change
dateToInsert = datetime.today() - timedelta(days=2)
dateToInsert = dateToInsert.strftime('%Y-%m-%d')


urlCase = "https://epistat.sciensano.be/Data/COVID19BE_CASES_AGESEX.json"
urlHosp = "https://epistat.sciensano.be/Data/COVID19BE_HOSP.json"
urlDeath = "https://epistat.sciensano.be/Data/COVID19BE_MORT.json"
urlTest = "https://epistat.sciensano.be/Data/COVID19BE_tests.json"



db = MySQLdb.connect(host="127.0.0.1",db="coviddb", read_default_file="/etc/mysql/my.cnf");
cur = db.cursor()


def url_getJSON(url):
    try:
        with requests.get(url) as r:
            data = r.json()
            return data
    except:
        print(f"Error loading {url}")
        exit()	


def getProvinceID(provinceName):
	cur.execute(f'SELECT provinceID FROM provinces WHERE provinceName = \'{provinceName}\'')
	result = cur.fetchone()
	return result[0]
	
	
def getRegionID(regionName):
	cur.execute(f'SELECT regionID FROM regions WHERE regionName = \'{regionName}\'')
	result = cur.fetchone()
	return result[0]

# ------------------------------
# Start function read json tests 
def readTest():
	dataset = url_getJSON(urlTest)
	# Iteratie through every JSON object
	for data in dataset:
		try:
			date = data['DATE']
			testAll = data['TESTS_ALL']
			testPos = data['TESTS_ALL_POS']
			# If an error occurs in reading the JSON, stop the reading
			
			# If the key 'PROVINCE' exists
			if ('PROVINCE' in data):
				# Get provinceID & regionID
				provinceID = getProvinceID(data['PROVINCE'])
				regionID = getRegionID(data['REGION'])
				

				#Check if the object already exists
				sql = 'SELECT * FROM tests WHERE testDate = %s AND testProvinceID = %s AND testRegionID = %s'
				val = (date,provinceID,regionID)
				cur.execute(sql,val)
				print(cur.rowcount)
				# If the object does not exists, insert into db
				if (cur.rowcount == 0):
					# Check if date is older than 2 days from now
						try:
							sql = "INSERT INTO tests(testDate,testProvinceID,testRegionID,testAll,testPos) VALUES (%s,%s,%s,%s,%s)"
							val = (date,provinceID,regionID,testAll,testPos)
							cur.execute(sql,val)
							db.commit()
						except:
							print("Error (101) - inserting test")
							
			# If regionID & provinceID do not exist
			else:
				#Check if object exists
				sql = "SELECT * FROM tests WHERE testDate = %s AND testProvinceID = %s AND testRegionID = %s"
				val = (data['DATE'], '1', '1')
				cur.execute(sql,val)
				if (cur.rowcount == 0):
					# Check if date is older than 2 days from now
					if (date < dateToInsert):
						try:
							sql = "INSERT INTO tests(testDate,testProvinceID,testRegionID,testAll,testPos) VALUES (%s,%s,%s,%s,%s)"
							val = (date,'1','1',testAll,testPos)
							cur.execute(sql,val)
							db.commit()
						except:
							print("Error(102) - inserting test")

		except:
			print('JSON FILE IS BROKEN - '+urlTest)
			exit()
# End function read json tests
# ------------------------------
# Start function read json hosps
def readHosp():
	dataset = url_getJSON(urlHosp)
	for data in dataset:
		try:
			hospDate = data['DATE']
			hospProvinceID = getProvinceID(data['PROVINCE'])
			hospRegionID = getRegionID(data['REGION'])
			totalInHosp = data['TOTAL_IN']
			totalInICU = data['TOTAL_IN_ICU']
			totalInResp = data['TOTAL_IN_RESP']
			newInHosp = data['NEW_IN']
			newOutHosp = data['NEW_OUT']
			
			# Check if object already exists
			sql= 'SELECT * FROM hosps WHERE hospDate = %s AND hospProvinceID = %s AND hospRegionID = %s'
			val = (hospDate, hospProvinceID, hospRegionID)
			cur.execute(sql,val)
			
			# If object is not in DB, insert
			if (cur.rowcount == 0):
				#Check if data is older than 2 days from now
				if (hospDate < dateToInsert):
					try:
						sql = "INSERT INTO hosps(hospDate,hospProvinceID,hospRegionID,totalInHosp,totalInICU,totalInResp,newInHosp,newOutHosp) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"
						val = (hospDate,hospProvinceID,hospRegionID,totalInHosp,totalInICU,totalInResp,newInHosp,newOutHosp)
						cur.execute(sql,val)
						db.commit()
					except:
						print("Error(102) - insertings hosps")
						
		except:
			print('JSON FILE IS BROKEN - '+urlHosp)
			exit()
			
# End function read json hosps
# -------------------------------
# Start function read json deaths
def readDeath():
	dataset = url_getJSON(urlDeath)
	for data in dataset:
		try:
			specialCase = 0
			deathDate = data['DATE']
			deathRegionID = getRegionID(data['REGION'])
			deaths = data['DEATHS']

			# Check if key 'AGEGROUP' exists
			if ('AGEGROUP' in data):
				deathAgeGroup = data['AGEGROUP']
			else:
				deathAgeGroup = None
				specialCase = 1
				
			# Check if key 'SEX' exists.
			if ('SEX' in data):
				deathSex = data['SEX']
			else:
				deathSex = None
				specialCase = 1
			
			# The Select query is different if one or more values are None
			if (specialCase == 0):
				sql= 'SELECT * FROM deaths WHERE deathDate = %s AND deathRegionID = %s AND deathAgeGroup = %s AND deathSex = %s'
				val = (deathDate,deathRegionID,deathAgeGroup, deathSex)
				cur.execute(sql,val)
		
			else:
				if (deathAgeGroup == None and deathSex == None):
					sql = 'SELECT * FROM deaths WHERE deathDate = %s AND deathRegionID = %s AND deathAgeGroup IS NULL AND deathSex IS NULL'
					val = (deathDate,deathRegionID)
					cur.execute(sql,val)
				elif (deathAgeGroup == None):
					sql = 'SELECT * FROM deaths WHERE deathDate = %s AND deathRegionID = %s AND deathAgeGroup IS NULL AND deathSex = %s'
					val = (deathDate,deathRegionID, deathSex)
					cur.execute(sql,val)
				else:
					sql = 'SELECT * FROM deaths WHERE deathDate = %s AND deathRegionID = %s AND deathAgeGroup = %s AND deathSex IS NULL'
					val = (deathDate,deathRegionID,deathAgeGroup)
					cur.execute(sql,val)
			
			# Check if the object already exists
			if (cur.rowcount == 0):
				
				#Check if data is older than 2 days from now
				if (deathDate < dateToInsert):
					try:
						sql = 'INSERT INTO deaths(deathDate,deathRegionID,deathAgeGroup, deathSex, deaths) VALUES (%s,%s,%s,%s,%s)'
						val = (deathDate,deathRegionID,deathAgeGroup,deathSex,deaths)
						cur.execute(sql,val)
						db.commit()

					except:
						print("Error(102) - insertings deaths")
						
		except:
			print('JSON FILE IS BROKEN - '+urlDeath)
			exit()
# End function read json deaths
# ------------------------------
# Start function read json cases
def readCase():
	dataset = url_getJSON(urlCase)
	for data in dataset:
		try:
			cases = data['CASES']
			
			# Check if key 'DATE' exists
			if ('DATE' in data):
				caseDate = data['DATE']
			else:
				caseDate = None

			# Check if key 'AGEGROUP' exists
			if ('AGEGROUP' in data):
				caseAgeGroup = data['AGEGROUP']
			else:
				caseAgeGroup = None
			
			# Check if 'PROVINCE' exists
			if ('PROVINCE' in data):
				caseProvinceID = getProvinceID(data['PROVINCE'])
			else:
				caseProvinceID = 1
			
			# Check if 'REGION' exists	
			if ('REGION' in data):
				caseRegionID = getRegionID(data['REGION'])
			else:
				caseRegionID = 1
				
			# Check if 'SEX' exists
			if ('SEX' in data):
				caseSex = data['SEX']	
			else:
				caseSex = None
			
			# If one or more values are None, the SELECT query is different
			if (caseDate == None and caseAgeGroup == None and caseSex == None):
				sql = 'SELECT * FROM cases WHERE caseDate IS NULL AND caseProvinceID = %s AND caseRegionID = %s AND caseAgeGroup IS NULL AND caseSex IS NULL'
				val = (caseProvinceID, caseRegionID)
				cur.execute(sql,val)
				
			elif (caseDate == None and caseAgeGroup == None):
				sql = 'SELECT * FROM cases WHERE caseDate IS NULL AND caseProvinceID = %s AND caseRegionID = %s AND caseAgeGroup IS NULL AND caseSex = %s'
				val = (caseProvinceID,caseRegionID,caseSex)
				cur.execute(sql,val)
				
			elif (caseDate == None and caseSex == None):
				sql = 'SELECT * FROM cases WHERE caseDate IS NULL AND caseProvinceID = %s AND caseRegionID = %s AND caseAgeGroup = %s AND caseSex IS NULL'
				val = (caseProvinceID, caseRegionID,caseAgeGroup)
				cur.execute(sql,val)
				
			elif (caseAgeGroup == None and caseSex == None):
				sql = 'SELECT * FROM cases WHERE caseDate = %s AND caseProvinceID = %s AND caseRegionID = %s AND caseAgeGroup IS NULL AND caseSex IS NULL'
				val = (caseDate,caseProvinceID, caseRegionID)
				cur.execute(sql,val)
				
			elif (caseAgeGroup == None):
				sql = 'SELECT * FROM cases WHERE caseDate = %s AND caseProvinceID = %s AND caseRegionID = %s AND caseAgeGroup IS NULL AND caseSex = %s'
				val = (caseDate,caseProvinceID, caseRegionID,caseSex)
				cur.execute(sql,val)
			
			elif (caseSex == None):
				sql = 'SELECT * FROM cases WHERE caseDate = %s AND caseProvinceID = %s AND caseRegionID = %s AND caseAgeGroup = %s AND caseSex IS NULL'
				val = (caseDate,caseProvinceID,caseRegionID,caseAgeGroup)
				cur.execute(sql,val)
				
			elif (caseDate == None):
				sql = 'SELECT * FROM cases WHERE caseDate IS NULL AND caseProvinceID = %s AND caseRegionID = %s AND caseAgeGroup = %s AND caseSex = %s'
				val = (caseProvinceID, caseRegionID,caseAgeGroup, caseSex)
				cur.execute(sql,val)
				
			else:
				sql= 'SELECT * FROM cases WHERE caseDate = %s AND caseProvinceID = %s AND caseRegionID = %s AND caseAgeGroup = %s AND caseSex = %s'
				val = (caseDate,caseProvinceID,caseRegionID,caseAgeGroup,caseSex)	
				cur.execute(sql,val)
			
			# Check if object already exists
			if (cur.rowcount == 0):
				# If the object is not in the DB, insert it
				# Check if date is older than 2 days from now
				# If this is not the case, the numbers are not correct
				if (caseDate == None):
					sql = "INSERT INTO cases(caseDate,caseProvinceID,caseRegionID,caseAgeGroup,caseSex,cases) VALUES (%s,%s,%s,%s,%s,%s)"
					val = (caseDate,caseProvinceID,caseRegionID,caseAgeGroup,caseSex,cases)
					cur.execute(sql,val)
					db.commit()
					
				elif (caseDate < dateToInsert):
					try:
						sql = "INSERT INTO cases(caseDate,caseProvinceID,caseRegionID,caseAgeGroup,caseSex,cases) VALUES (%s,%s,%s,%s,%s,%s)"
						val = (caseDate,caseProvinceID,caseRegionID,caseAgeGroup,caseSex,cases)
						cur.execute(sql,val)
						db.commit()

					except:
						print("Error(102) - insertings cases")

		except:
			print('JSON FILE IS BROKEN - '+urlCase)
			print(data)
			exit()
# End function read json cases
# ----------------------------

def main():
	readHosp()
	readTest()
	readDeath()
	readCase()

if __name__ == "__main__":
    	main()
