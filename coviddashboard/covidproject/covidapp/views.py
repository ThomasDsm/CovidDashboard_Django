from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader

from .models import Regions, Cases, Provinces, Hosps, Tests
import datetime
import sys

def index(request):
	template = loader.get_template('covidapp/index.html')
	return HttpResponse(template.render())
	
def regions(request):
	output=Regions.objects.get(regionname='Flanders').regionname
	for region in Regions.objects.all():
		output+= region.regionname
	return HttpResponse(output)

def prov(request):
	province = request.GET.get('prov')
	try:
		provid = Provinces.objects.get(provincename=province).provinceid
	except:
		return HttpResponse("Provintie niet gevonden")
		
	#Get date to start, is today -2 for data accuracy, then go to start of timespan to analyze
	date = datetime.date.today()
	datestart = date - datetime.timedelta(days=(2+14+2))
	datestop = date - datetime.timedelta(days=(2))
	
	datecases = datestart + datetime.timedelta(days=1)
	datehosps = datestart + datetime.timedelta(days=1)
	datepos = datestart + datetime.timedelta(days=1)
	
	casesdate = []
	totalCases = 0
	#Get case data for selected province over last 14 days
	for i in range(14):
		sumcases = 0
		#Add all cases from diffirent Sex, agegroup
		cases = Cases.objects.filter(casedate=datecases, caseprovinceid=provid)
		for case in cases:
			sumcases += case.cases
		totalCases += sumcases
		#make list of tuples with date and number of cases
		casesitem = (datecases.strftime("%d-%m-%y"), sumcases)
		casesdate.append(casesitem)	
		datecases += datetime.timedelta(days=1)
	
	#Get total hospital admissions over last 14 days
	totaladms = 0
	hospadms = Hosps.objects.filter(hospdate__gt=datestart, hospdate__lt=datestop, hospprovinceid=provid)
	for hospadm in hospadms:
		totaladms += hospadm.newinhosp
	
		
	#Get hospital data for selected povince over last 14 days
	hospsdate = []
	for i in range(14):
		#Get number of hospitalisations
		hosps = Hosps.objects.get(hospdate=datehosps, hospprovinceid=provid).totalinhosp
		#make list of tuples with date and number of hosps
		hospsitem = (datehosps.strftime("%d-%m-%y"), hosps)
		hospsdate.append(hospsitem)	
		datehosps += datetime.timedelta(days=1)
		
	#Get posRate for selected povince over last 14 days
	posRateDate = []
	totalTests = 0
	for i in range(14):
		#Get test data
		testobj = Tests.objects.get(testdate=datepos, testprovinceid=provid)
		#Get positivity ratio, in percent
		posRate = casesdate[i][1] / testobj.testall * 100
		totalTests += testobj.testall
		#make list of tuples with date and pos ratio
		posRateItem = (datepos.strftime("%d-%m-%y"), posRate)
		posRateDate.append(posRateItem)	
		datepos += datetime.timedelta(days=1)
		
	#Average positivity ratio, based on total cass and total tests calculated previously
	avgPosRate = totalCases / totalTests * 100
		
	#get case data for all provinces
	casesprov = []
	for provid in range(1, 13):
		totalcases = 0;
		provname = Provinces.objects.get(provinceid=provid).provincename
		cases = Cases.objects.filter(casedate__gt=datestart, casedate__lt=datestop, caseprovinceid=provid)
		#Sum all cases from a province over date range
		for case in cases:
			totalcases += case.cases
			
		item = (provname, totalcases)
		casesprov.append(item)
		
	if province == 'VlaamsBrabant':
		provincename = 'Vlaams Brabant'
	elif province == 'WestVlaanderen':
		provincename = 'West Vlaanderen'
	elif province == 'OostVlaanderen':
		provincename = 'Oost Vlaanderen'
	elif province == 'OostVlaanderen':
		provincename = 'Oost Vlaanderen'
	elif province == 'BrabantWallon':
		provincename = 'Brabant Wallon'
	else:
		provincename = province
	
	d = {'casesdate': casesdate, 'casesprov': casesprov, 'hospsdate': hospsdate, 'posratedate': posRateDate, 'provname': provincename, 'totaladms': totaladms, 'avgposrate': avgPosRate, 'totalcases': totalCases, 'totaltests': totalTests}
	
	template = loader.get_template('covidapp/province.html')
	return HttpResponse(template.render(d))
	
def reg(request):
	region = request.GET.get('reg')
	try:
		regid = Regions.objects.get(regionname=region).regionid
	except:
		return HttpResponse("Regio niet gevonden")
	
	#Get date, is today -2 for data accuracy, then go to start of timespan to analyze
	date = datetime.date.today()
	datestart = date - datetime.timedelta(days=(17))
	datestop = date - datetime.timedelta(days=(2))
	
	''' CASES '''
	casesdate = []
	totalcases = 0
	#Get case data for selected region over last 14 days
	cases = Cases.objects.filter(casedate__gt=datestart, casedate__lt=datestop, caseregionid=regid)
	for case in cases:
		totalcases += case.cases
		
	'''HOSPITALISATIONS'''
	#Get hospital data for selected region over last 14 days
	hospsdate = []
	totalhosps = 0
	hosps = Hosps.objects.filter(hospdate__gt=datestart, hospdate__lt=datestop, hospregionid=regid)
	for hosp in hosps:
		totalhosps += hosp.newinhosp
		
	'''TESTS'''
	#Get posRate for selected povince over last 14 days
	testscount = 0
	tests = Tests.objects.filter(testdate__gt=datestart, testdate__lt=datestop, testregionid=regid)
	for test in tests:
		testscount += test.testall
			
	posRate = totalcases / testscount * 100
		
	'''CASES COMPARISON'''
	#get case data for all regions
	casesreg = []
	#Loop for every region
	for regid in range(1, 5):
		sumcases = 0; #Reset
		regname = Regions.objects.get(regionid=regid).regionname #Get name to put in chart
		if regname==None:
			regname='Onbekend'
		elif regname=='Flanders':
			regname='Vlaanderen'
		elif regname=='Wallonia':
			regname='Wallonië'
		elif regname=='Brussels':
			regname='Brussel'
			
		cases = Cases.objects.filter(casedate__gt=datestart, casedate__lt=datestop, caseregionid=regid) #Get case object
		#Sum all cases
		for case in cases:
			sumcases += case.cases
			
		item = (regname, sumcases) #Add to list
		casesreg.append(item)
		
	#Translate region name
	if region=='Flanders':
		region='Vlaanderen'
	elif region=='Wallonia':
		region='Wallonië'
	elif region=='Brussels':
		region='Brussel'
		
	#Make dictionary to pass to template renderer
	d = {'casesreg': casesreg, 'posrateavg': posRate, 'totalhosps': totalhosps, 'totalcases': totalcases, 'totaltest': testscount, 'regionname': region}
	template = loader.get_template('covidapp/region.html')
	return HttpResponse(template.render(d))
	
