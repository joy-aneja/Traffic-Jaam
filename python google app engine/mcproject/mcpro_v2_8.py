from google.appengine.ext import db
from datetime import datetime, timedelta

import string
import webapp2

import urllib2
import json
import logging
from xml.dom.minidom import Document
from xml.dom import minidom

from datetime import datetime, timedelta, date

from pytz.gae import pytz 
from pytz import timezone

import logging



source = "28.549291,77.267814"
dest = "28.556162,77.099958"

source_coord = []
dest_coord = []


def convert_ts_table():
	
	#to_zone = tz.gettz('Asia/Kolkata')
	#route = Route(source = "ts", dest = "ts")
	#r_key = route.put()
	#rt = route.getRoute(r_key)

	ind = datetime.now(timezone('Asia/Kolkata'))
	
	
	return ind.isocalendar()[1], ind.weekday(), ind.hour

def new_date():

	for i in range(8,24):
			#exec("obj = Time_"+str(i)+"(source ="+str(source)+", dest ="+str(dest)+")")
			exec("route = Time_"+str(i)+"(source ='date', dest ='date')")
			#obj = Time_9(source = source, dest = dest)	    
			route.put()

def update_date(hr,wk,day):
		w1=[]
		w2=[]
		result_row = db.GqlQuery("select * from Time_"+str(hr)+" where source = 'date' AND dest = 'date' LIMIT 1")
		list_row = result_row.get()
		for j in result_row:
			  for k in range(0,7):
				  exec("w1.append(j.day1_"+str(k)+")")
				  exec("w2.append(j.day2_"+str(k)+")")

			  source = j.source
			  dest = j.dest
			  if wk == 1:
				  w1[day] = str(datetime.now(timezone('Asia/Kolkata')))
			  else:
				  w2[day] = str(datetime.now(timezone('Asia/Kolkata'))) 


		db.delete(list_row)
		exec("route = Time_"+str(hr)+"(source = source, dest = dest, day1_0 = str(w1[0]), day1_1 = str(w1[1]), day1_2 = str(w1[2]), day1_3 = str(w1[3]), day1_4 = str(w1[4]), day1_5 = str(w1[5]), day1_6 = str(w1[6]), day2_0 = str(w2[0]), day2_1 = str(w2[1]), day2_2 = str(w2[2]), day2_3 = str(w2[3]), day2_4 = str(w2[4]), day2_5 = str(w2[5]), day2_6 = str(w2[6]))")
		route.put()



class MainPage(webapp2.RequestHandler):
	def get(self):
		self.response.headers['Content-Type'] = 'text/html'
		self.response.write("<br/><br/>")
		self.response.write("Welcome to MC Project testing...")
		source = "28.549291,77.267814"
		dest = "28.556162,77.099958"
		source1 = "28.657839,77.142476"
		dest1 = "28.566008,77.176743"
		source_coord.append(source)
		source_coord.append(source1)
		dest_coord.append(dest)
		dest_coord.append(dest1)
		self.response.write(source_coord)
		self.response.write(" ")
		self.response.write(dest_coord)
		self.response.write(source_coord[0])
		self.response.write(dest_coord[0])
		

class addDate(webapp2.RequestHandler):
	def get(self):
		new_date()
		self.response.write("date row added")


class NewRoute(webapp2.RequestHandler):
	def get(self):
		source = self.request.get('source')
		dest = self.request.get('dest')
		self.addRoute(source, dest)
		


	def addRoute(self, source, dest):
		route = Route(source = source, dest = dest)
		route.put()			
		for i in range(8,24):
			#exec("obj = Time_"+str(i)+"(source ="+str(source)+", dest ="+str(dest)+")")
			exec("route = Time_"+str(i)+"(source = source, dest = dest)")
			#obj = Time_9(source = source, dest = dest)	    
			route.put()	


class GetDigest(webapp2.RequestHandler):
	
	def get(self):
		self.response.headers['Content-Type'] = "text/html; charset=iso-8859-1"
		hour = self.request.get('hour')
		
		src = self.request.get('source')
		dst = self.request.get('dest')
		wk = datetime.now(timezone('Asia/Kolkata')).isocalendar()[1]
		wk = wk % 2 + 1
		self.createDigest(hour,src,dst,wk)
		day = datetime.now(timezone('Asia/Kolkata')).weekday()
		


	def createDigest(self, hour, source, dest, wk):
		

		w1=[]
		w2=[]
		date1=[]
		date2=[]
		digest=""
		result_row = db.GqlQuery("select * from Time_"+str(hour)+" where source = '" +source+ "' AND dest = '" +dest+ "' LIMIT 1")
		list_row = result_row.get()
		for j in result_row:
			  for k in range(0,7):
				  exec("w1.append(j.day1_"+str(k)+")") in globals(), locals()
				  exec("w2.append(j.day2_"+str(k)+")")
			  est_val = str(j.lfd_avg)
			  #source = j.source
			  #dest = j.dest
			  #if wk == 1:
				 # w1[day] = str(toj)
			  #else:
				 # w2[day] = str(toj) 
		
		date_row = db.GqlQuery("select * from Time_"+str(hour)+" where source = 'date' AND dest = 'date' LIMIT 1")
		list_date = date_row.get()

		for x in date_row:
			  for y in range(0,7):
				  exec("date1.append(x.day1_"+str(y)+")")
				  exec("date2.append(x.day2_"+str(y)+")")

        
		digest= """{
						"data":{
							
							"week":\"""" + str(wk) +"""\",
							"hour":\"""" + str(hour) +"""\",
	
							"week1":
							{ 
					
					
							"toj":[{"day":"0","date":\""""+str(date1[0])+"""\","toj":\""""+str(w1[0])+"""\"},{"day":"1","date":\""""+str(date1[1])+"""\","toj":\""""+str(w1[1])+"""\"},{"day":"2","date":\""""+str(date1[2])+"""\","toj":\""""+str(w1[2])+"""\"},{"day":"3","date":\""""+str(date1[3])+"""\","toj":\""""+str(w1[3])+"""\"},{"day":"4","date":\""""+str(date1[4])+"""\","toj":\""""+str(w1[4])+"""\"},{"day":"5","date":\""""+str(date1[5])+"""\","toj":\""""+str(w1[5])+"""\"},{"day":"6","date":\""""+str(date1[6])+"""\","toj":\""""+str(w1[6])+"""\"}]},
		  
							"week2":    
							{
					
					
							"toj":[{"day":"0","date":\"""" +str(date2[0])+ """\","toj":\""""+str(w2[0])+"""\"},{"day":"1","date":\""""+str(date2[1])+"""\","toj":\""""+str(w2[1])+"""\"},{"day":"2","date":\""""+str(date2[2])+"""\","toj":\""""+str(w2[2])+"""\"},{"day":"3","date":\""""+str(date2[3])+"""\","toj":\""""+str(w2[3])+"""\"},{"day":"4","date":\""""+str(date2[4])+"""\","toj":\""""+str(w2[4])+"""\"},{"day":"5","date":\""""+str(date2[5])+"""\","toj":\""""+str(w2[5])+"""\"},{"day":"6","date":\""""+str(date2[6])+"""\","toj":\""""+str(w2[6])+"""\"}]}
		
							
						   , "estimatedtoj":\""""+ str(est_val)+"""\"
								}
                                ,"cday":\"""" + str(1) +"""\"}"""

		self.response.write(digest)



class TrafficAppHandler(webapp2.RequestHandler):
	
	rt = None		
	def getToj(self):
		curr_day = 0
		##28.545926,77.270579
		##28.527829,77.205799
		source = "28.549291,77.267814"
		dest = "28.556162,77.099958"
		wk, day , hr =	convert_ts_table()
		self.response.write(str(wk))

		
		

		#exec("route = Time_"+str(hr)+"(source = source, dest = dest, day"+str(wk)+"_"+str(day)+" = str(toj))")
		#route.put()

		#route.put()
		#r_key = route.put()

		#rt = route.getTime_8(r_key)
		#self.response.write("source: " + rt.source + "<br\>dest: " + rt.dest + "<br\>toj: " + str(rt.toj) + "<br\>Ts: " + str(rt.ts))
		
		
		self.response.write(str(day)+" "+str(hr))
		#self.response.write("select * from Time_"+str(8))
		#query="select * from Time_"+str(8) 
		#result = db.GqlQuery(query)
		#where_cond="where source = '" + source + "' AND dest = '" + dest + "' LIMIT 1"
		#exec("result = Time_"+str(hr)+".gql(where_cond)")
		result = db.GqlQuery("select * from Route")
		result = list(result)
		wk  = (wk % 2) + 1
		
		for rt in result:
			source = rt.source
			dest = rt.dest
			w1 = []
			w2 = []
			contents = urllib2.urlopen("http://route.cit.api.here.com/routing/7.2/calculateroute.json?app_id=<your_app_id>&app_code=<your_App_code>&waypoint0=geo!" + source + "&waypoint1=geo!" + dest + "&mode=fastest;car;traffic:enabled").read()
			trafficData = json.loads(contents)
			toj = trafficData["response"]["route"][0]["summary"]["trafficTime"]
			result_row = db.GqlQuery("select * from Time_"+str(hr)+" where source = '" + source + "' AND dest = '" + dest + "' LIMIT 1")
			list_row = result_row.get()
			for j in result_row:
				for k in range(0,7):
					exec("w1.append(j.day1_"+str(k)+")")
					exec("w2.append(j.day2_"+str(k)+")")
				logging.info("w1 "+ str(w1) +" w2"+str(w2))
				source = j.source
				dest = j.dest
				if wk == 1:
					w1[day] = str(toj)
				else:
					w2[day] = str(toj)
				logging.info(str(list_row))
				db.delete(list_row)
				exec("route = Time_"+str(hr)+"(source = source, dest = dest, day1_0 = str(w1[0]), day1_1 = str(w1[1]), day1_2 = str(w1[2]), day1_3 = str(w1[3]), day1_4 = str(w1[4]), day1_5 = str(w1[5]), day1_6 = str(w1[6]), day2_0 = str(w2[0]), day2_1 = str(w2[1]), day2_2 = str(w2[2]), day2_3 = str(w2[3]), day2_4 = str(w2[4]), day2_5 = str(w2[5]), day2_6 = str(w2[6]))")
				route.put()
		self.estimation(hr, day, source, dest)
		update_date(hr,wk,day)
		
		logging.info("day="+str(day)+" curr_day="+str(curr_day))
		


		
	
	def estimation(self, hr, day, source, dest):
		self.response.write("estimating...")
		wk1=[]
		wk2=[]
		values=[]
		deltas=[]
		weights_1=[0,0.125,0.0625,0.003125,0.0015625,0.00078125,0.00078125,0.5,0.125,0.0625,0.003125,0.0015625,0.00078125,0.00078125]
		weights_2=[0,0.126984127,0.063492063,0.03174603,0.015873016,0.00793650,0.003968,0.5,0.126984127,0.063492063,0.03174603,0.015873016,0.00793650,0.003968]
		result = db.GqlQuery("select * from Route")
		result = list(result)
		
		
		for rt in result:
			source = rt.source
			dest = rt.dest
			result_row = db.GqlQuery("select * from Time_"+str(hr)+" where source = '" + str(source) + "' AND dest = '" + str(dest) + "' LIMIT 1")
			list_row = result_row.get()
			logging.info(list_row)
			for q in result_row:
				wk1=[]
				wk2=[]
				values=[]
				for w in range(0,7):
					exec("a1 = q.day1_"+str(w))
					exec("a2 = q.day2_"+str(w))
					wk1.append(a1)
					wk2.append(a2)
				for j in range(0,7):
					if wk1[j] != 'None':
						values.append(wk1[j])
					else :
						values.append(str(0))
				for j in range(0,7):
					if wk2[j] != 'None':
						values.append(wk2[j])
					else :
						values.append(str(0))
				logging.info(str(values))
				wk = datetime.now(timezone('Asia/Kolkata')).isocalendar()[1]
				wk = wk % 2 + 1
				if wk == 2:
					k =  7 + day
				else:
					k = day
				toj = values[k]
				self.response.write("k ="+str(k))
				deltas=[]
				for j in range(0,14):
					deltas.append(int(values[(k+1)%14]) - int(values[k]))
					k = k-1
				self.response.write(str(values)+"\n")
				self.response.write(str(deltas))
				est_val1 = 0
				est_val2 = 0
				est_del_1 = 0
				est_del_2 = 0
				self.response.write("the day is " + str(day))
				for f in range(0,14):
					est_del_1 = est_del_1 + (deltas[f] * weights_1[f])
					est_del_2 = est_del_2 + (deltas[f] * weights_2[f])
				self.response.write("est delta 1: " + str(est_del_1))
				self.response.write("est delta 2: " + str(est_del_2))
				est_val1 = int(toj) + est_del_1
				est_val2 = int(toj) + est_del_2
				self.response.write("est value 1: " + str(est_val1))
				self.response.write("est value 2: " + str(est_val2))
				db.delete(list_row)
				exec("route = Time_"+str(hr)+"(source = source, dest = dest, day1_0 = str(wk1[0]), day1_1 = str(wk1[1]), day1_2 = str(wk1[2]), day1_3 = str(wk1[3]), day1_4 = str(wk1[4]), day1_5 = str(wk1[5]), day1_6 = str(wk1[6]), day2_0 = str(wk2[0]), day2_1 = str(wk2[1]), day2_2 = str(wk2[2]), day2_3 = str(wk2[3]), day2_4 = str(wk2[4]), day2_5 = str(wk2[5]), day2_6 = str(wk2[6]),lfd_avg = str(est_val2))")
				route.put()		



	def get(self):
		self.response.headers['Content-Type'] = "text/html; charset=iso-8859-1"
		self.getToj()
		#route = Route(source = source, dest = dest, toj = str(toj))
		#r_key = route.put()
		#rt = route.getRoute(r_key)
		#self.response.write("source: " + rt.source + "<br\>dest: " + rt.dest + "<br\>toj: " + str(rt.toj) + "<br\>Ts: " + str(rt.ts))

		#data_log = Time_8am(source = source, dest = dest, toj = str(toj))
		#d_key = data_log.put()
		#data_ins = data_log.getTime_8(d_key)
		#self.response.write("from Time_8 source: " + rt.source + "<br\>dest: " +
		#rt.dest + "<br\>toj: " + str(rt.toj) + "<br\>Ts: " + str(rt.ts))

	
	
		
class RouteTimeHandler(webapp2.RequestHandler):
	def get(self):
		self.response.headers['Content-Type'] = "text/html; charset=iso-8859-1"
		source = self.request.get("source")
		dest = self.request.get("dest")
		result = db.GqlQuery("select * from Route where source = '" + source + "' AND dest = '" + dest + "'")
		result = list(result)
		JsonObj = {"route" : {"source" : source, "dest" : dest}, "toj" : []}
		for rt in result:
			JsonObj["toj"].append({"ts" : str(rt.ts), "time" : rt.toj})
		json_output = json.dumps(JsonObj)
		self.response.write(json_output)
		

class Route(db.Model):
	source = db.StringProperty(required = True)
	dest = db.StringProperty(required = False)
	
	
	def getRoute(self, key):
		return db.get(key)



class Time_8(db.Model):
   
	#day = db.StringProperty(required = True,
	#choices=set(["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]))
	day1_0  = db.StringProperty(required = False)
	day1_1  = db.StringProperty(required = False)
	day1_2  = db.StringProperty(required = False)
	day1_3  = db.StringProperty(required = False)
	day1_4  = db.StringProperty(required = False)
	day1_5  = db.StringProperty(required = False)
	day1_6  = db.StringProperty(required = False)
	
	day2_0  = db.StringProperty(required = False)
	day2_1  = db.StringProperty(required = False)
	day2_2  = db.StringProperty(required = False)
	day2_3  = db.StringProperty(required = False)
	day2_4  = db.StringProperty(required = False)
	day2_5  = db.StringProperty(required = False)
	day2_6  = db.StringProperty(required = False)
	
	lfd_avg = db.StringProperty(required=False)
	source = db.StringProperty(required = False)
	dest = db.StringProperty(required = False)
	
	def getTime_8(self, key):
		return db.get(key)
 
class Time_9(db.Model):
   
	#day = db.StringProperty(required = False,
	#choices=set(["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]))
	day1_0  = db.StringProperty(required = False)
	day1_1  = db.StringProperty(required = False)
	day1_2  = db.StringProperty(required = False)
	day1_3  = db.StringProperty(required = False)
	day1_4  = db.StringProperty(required = False)
	day1_5  = db.StringProperty(required = False)
	day1_6  = db.StringProperty(required = False)
	
	day2_0  = db.StringProperty(required = False)
	day2_1  = db.StringProperty(required = False)
	day2_2  = db.StringProperty(required = False)
	day2_3  = db.StringProperty(required = False)
	day2_4  = db.StringProperty(required = False)
	day2_5  = db.StringProperty(required = False)
	day2_6  = db.StringProperty(required = False)

	lfd_avg = db.StringProperty(required=False)
	source = db.StringProperty(required = False)
	dest = db.StringProperty(required = False)
	
	def getTime_9(self,key):
		return db.get(key)
		
		
		
class Time_10(db.Model):
   
	#day = db.StringProperty(required = False,
	#choices=set(["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]))
	day1_0  = db.StringProperty(required = False)
	day1_1  = db.StringProperty(required = False)
	day1_2  = db.StringProperty(required = False)
	day1_3  = db.StringProperty(required = False)
	day1_4  = db.StringProperty(required = False)
	day1_5  = db.StringProperty(required = False)
	day1_6  = db.StringProperty(required = False)
	
	day2_0  = db.StringProperty(required = False)
	day2_1  = db.StringProperty(required = False)
	day2_2  = db.StringProperty(required = False)
	day2_3  = db.StringProperty(required = False)
	day2_4  = db.StringProperty(required = False)
	day2_5  = db.StringProperty(required = False)
	day2_6  = db.StringProperty(required = False)

	lfd_avg = db.StringProperty(required=False)
	source = db.StringProperty(required = False)
	dest = db.StringProperty(required = False)
	
	def getTime_10(self,key):
		return db.get(key)
		
		
class Time_11(db.Model):
   
	#day = db.StringProperty(required = False,
	#choices=set(["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]))
	day1_0  = db.StringProperty(required = False)
	day1_1  = db.StringProperty(required = False)
	day1_2  = db.StringProperty(required = False)
	day1_3  = db.StringProperty(required = False)
	day1_4  = db.StringProperty(required = False)
	day1_5  = db.StringProperty(required = False)
	day1_6  = db.StringProperty(required = False)
	
	day2_0  = db.StringProperty(required = False)
	day2_1  = db.StringProperty(required = False)
	day2_2  = db.StringProperty(required = False)
	day2_3  = db.StringProperty(required = False)
	day2_4  = db.StringProperty(required = False)
	day2_5  = db.StringProperty(required = False)
	day2_6  = db.StringProperty(required = False)

	lfd_avg = db.StringProperty(required=False)
	source = db.StringProperty(required = False)
	dest = db.StringProperty(required = False)
	
	def getTime_11(self,key):
		return db.get(key)
		
		
class Time_12(db.Model):
   
	#day = db.StringProperty(required = False,
	#choices=set(["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]))
	day1_0  = db.StringProperty(required = False)
	day1_1  = db.StringProperty(required = False)
	day1_2  = db.StringProperty(required = False)
	day1_3  = db.StringProperty(required = False)
	day1_4  = db.StringProperty(required = False)
	day1_5  = db.StringProperty(required = False)
	day1_6  = db.StringProperty(required = False)
	
	day2_0  = db.StringProperty(required = False)
	day2_1  = db.StringProperty(required = False)
	day2_2  = db.StringProperty(required = False)
	day2_3  = db.StringProperty(required = False)
	day2_4  = db.StringProperty(required = False)
	day2_5  = db.StringProperty(required = False)
	day2_6  = db.StringProperty(required = False)

	lfd_avg = db.StringProperty(required=False)
	source = db.StringProperty(required = False)
	dest = db.StringProperty(required = False)
	
	def getTime_12(self,key):
		return db.get(key)
		
		
		
class Time_13(db.Model):
   
	#day = db.StringProperty(required = False,
	#choices=set(["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]))
	day1_0  = db.StringProperty(required = False)
	day1_1  = db.StringProperty(required = False)
	day1_2  = db.StringProperty(required = False)
	day1_3  = db.StringProperty(required = False)
	day1_4  = db.StringProperty(required = False)
	day1_5  = db.StringProperty(required = False)
	day1_6  = db.StringProperty(required = False)
	
	day2_0  = db.StringProperty(required = False)
	day2_1  = db.StringProperty(required = False)
	day2_2  = db.StringProperty(required = False)
	day2_3  = db.StringProperty(required = False)
	day2_4  = db.StringProperty(required = False)
	day2_5  = db.StringProperty(required = False)
	day2_6  = db.StringProperty(required = False)

	lfd_avg = db.StringProperty(required=False)
	source = db.StringProperty(required = False)
	dest = db.StringProperty(required = False)
	
	def getTime_13(self,key):
		return db.get(key)
		
		
class Time_14(db.Model):
   
	#day = db.StringProperty(required = False,
	#choices=set(["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]))
	day1_0  = db.StringProperty(required = False)
	day1_1  = db.StringProperty(required = False)
	day1_2  = db.StringProperty(required = False)
	day1_3  = db.StringProperty(required = False)
	day1_4  = db.StringProperty(required = False)
	day1_5  = db.StringProperty(required = False)
	day1_6  = db.StringProperty(required = False)
	
	day2_0  = db.StringProperty(required = False)
	day2_1  = db.StringProperty(required = False)
	day2_2  = db.StringProperty(required = False)
	day2_3  = db.StringProperty(required = False)
	day2_4  = db.StringProperty(required = False)
	day2_5  = db.StringProperty(required = False)
	day2_6  = db.StringProperty(required = False)

	lfd_avg = db.StringProperty(required=False)
	source = db.StringProperty(required = False)
	dest = db.StringProperty(required = False)
	
	def getTime_14(self,key):
		return db.get(key)
		
		
class Time_15(db.Model):
   
	#day = db.StringProperty(required = False,
	#choices=set(["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]))
	day1_0  = db.StringProperty(required = False)
	day1_1  = db.StringProperty(required = False)
	day1_2  = db.StringProperty(required = False)
	day1_3  = db.StringProperty(required = False)
	day1_4  = db.StringProperty(required = False)
	day1_5  = db.StringProperty(required = False)
	day1_6  = db.StringProperty(required = False)
	
	day2_0  = db.StringProperty(required = False)
	day2_1  = db.StringProperty(required = False)
	day2_2  = db.StringProperty(required = False)
	day2_3  = db.StringProperty(required = False)
	day2_4  = db.StringProperty(required = False)
	day2_5  = db.StringProperty(required = False)
	day2_6  = db.StringProperty(required = False)

	lfd_avg = db.StringProperty(required=False)
	source = db.StringProperty(required = False)
	dest = db.StringProperty(required = False)
	
	def getTime_15(self,key):
		return db.get(key)
		
		
class Time_16(db.Model):
   
	#day = db.StringProperty(required = False,
	#choices=set(["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]))
	day1_0  = db.StringProperty(required = False)
	day1_1  = db.StringProperty(required = False)
	day1_2  = db.StringProperty(required = False)
	day1_3  = db.StringProperty(required = False)
	day1_4  = db.StringProperty(required = False)
	day1_5  = db.StringProperty(required = False)
	day1_6  = db.StringProperty(required = False)
	
	day2_0  = db.StringProperty(required = False)
	day2_1  = db.StringProperty(required = False)
	day2_2  = db.StringProperty(required = False)
	day2_3  = db.StringProperty(required = False)
	day2_4  = db.StringProperty(required = False)
	day2_5  = db.StringProperty(required = False)
	day2_6  = db.StringProperty(required = False)

	lfd_avg = db.StringProperty(required=False)
	source = db.StringProperty(required = False)
	dest = db.StringProperty(required = False)
	
	def getTime_16(self,key):
		return db.get(key)
		
		
class Time_17(db.Model):
   
	#day = db.StringProperty(required = False,
	#choices=set(["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]))
	day1_0  = db.StringProperty(required = False)
	day1_1  = db.StringProperty(required = False)
	day1_2  = db.StringProperty(required = False)
	day1_3  = db.StringProperty(required = False)
	day1_4  = db.StringProperty(required = False)
	day1_5  = db.StringProperty(required = False)
	day1_6  = db.StringProperty(required = False)
	
	day2_0  = db.StringProperty(required = False)
	day2_1  = db.StringProperty(required = False)
	day2_2  = db.StringProperty(required = False)
	day2_3  = db.StringProperty(required = False)
	day2_4  = db.StringProperty(required = False)
	day2_5  = db.StringProperty(required = False)
	day2_6  = db.StringProperty(required = False)

	lfd_avg = db.StringProperty(required=False)
	source = db.StringProperty(required = False)
	dest = db.StringProperty(required = False)
	
	def getTime_17(self,key):
		return db.get(key)
		
		
class Time_18(db.Model):
   
	#day = db.StringProperty(required = False,
	#choices=set(["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]))
	day1_0  = db.StringProperty(required = False)
	day1_1  = db.StringProperty(required = False)
	day1_2  = db.StringProperty(required = False)
	day1_3  = db.StringProperty(required = False)
	day1_4  = db.StringProperty(required = False)
	day1_5  = db.StringProperty(required = False)
	day1_6  = db.StringProperty(required = False)
	
	day2_0  = db.StringProperty(required = False)
	day2_1  = db.StringProperty(required = False)
	day2_2  = db.StringProperty(required = False)
	day2_3  = db.StringProperty(required = False)
	day2_4  = db.StringProperty(required = False)
	day2_5  = db.StringProperty(required = False)
	day2_6  = db.StringProperty(required = False)

	lfd_avg = db.StringProperty(required=False)
	source = db.StringProperty(required = False)
	dest = db.StringProperty(required = False)
	
	def getTime_18(self,key):
		return db.get(key)
		
		
class Time_19(db.Model):
   
	#day = db.StringProperty(required = False,
	#choices=set(["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]))
	day1_0  = db.StringProperty(required = False)
	day1_1  = db.StringProperty(required = False)
	day1_2  = db.StringProperty(required = False)
	day1_3  = db.StringProperty(required = False)
	day1_4  = db.StringProperty(required = False)
	day1_5  = db.StringProperty(required = False)
	day1_6  = db.StringProperty(required = False)
	
	day2_0  = db.StringProperty(required = False)
	day2_1  = db.StringProperty(required = False)
	day2_2  = db.StringProperty(required = False)
	day2_3  = db.StringProperty(required = False)
	day2_4  = db.StringProperty(required = False)
	day2_5  = db.StringProperty(required = False)
	day2_6  = db.StringProperty(required = False)

	lfd_avg = db.StringProperty(required=False)
	source = db.StringProperty(required = False)
	dest = db.StringProperty(required = False)
	
	def getTime_19(self,key):
		return db.get(key)
		
		
class Time_20(db.Model):
   
	#day = db.StringProperty(required = False,
	#choices=set(["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]))
	day1_0  = db.StringProperty(required = False)
	day1_1  = db.StringProperty(required = False)
	day1_2  = db.StringProperty(required = False)
	day1_3  = db.StringProperty(required = False)
	day1_4  = db.StringProperty(required = False)
	day1_5  = db.StringProperty(required = False)
	day1_6  = db.StringProperty(required = False)
	
	day2_0  = db.StringProperty(required = False)
	day2_1  = db.StringProperty(required = False)
	day2_2  = db.StringProperty(required = False)
	day2_3  = db.StringProperty(required = False)
	day2_4  = db.StringProperty(required = False)
	day2_5  = db.StringProperty(required = False)
	day2_6  = db.StringProperty(required = False)

	lfd_avg = db.StringProperty(required=False)
	source = db.StringProperty(required = False)
	dest = db.StringProperty(required = False)
	
	def getTime_20(self,key):
		return db.get(key)
		
		
class Time_21(db.Model):
   
	#day = db.StringProperty(required = False,
	#choices=set(["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]))
	day1_0  = db.StringProperty(required = False)
	day1_1  = db.StringProperty(required = False)
	day1_2  = db.StringProperty(required = False)
	day1_3  = db.StringProperty(required = False)
	day1_4  = db.StringProperty(required = False)
	day1_5  = db.StringProperty(required = False)
	day1_6  = db.StringProperty(required = False)
	
	day2_0  = db.StringProperty(required = False)
	day2_1  = db.StringProperty(required = False)
	day2_2  = db.StringProperty(required = False)
	day2_3  = db.StringProperty(required = False)
	day2_4  = db.StringProperty(required = False)
	day2_5  = db.StringProperty(required = False)
	day2_6  = db.StringProperty(required = False)

	lfd_avg = db.StringProperty(required=False)
	source = db.StringProperty(required = False)
	dest = db.StringProperty(required = False)
	
	def getTime_21(self,key):
		return db.get(key)
		
		
class Time_22(db.Model):
   
	#day = db.StringProperty(required = False,
	#choices=set(["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]))
	day1_0  = db.StringProperty(required = False)
	day1_1  = db.StringProperty(required = False)
	day1_2  = db.StringProperty(required = False)
	day1_3  = db.StringProperty(required = False)
	day1_4  = db.StringProperty(required = False)
	day1_5  = db.StringProperty(required = False)
	day1_6  = db.StringProperty(required = False)
	
	day2_0  = db.StringProperty(required = False)
	day2_1  = db.StringProperty(required = False)
	day2_2  = db.StringProperty(required = False)
	day2_3  = db.StringProperty(required = False)
	day2_4  = db.StringProperty(required = False)
	day2_5  = db.StringProperty(required = False)
	day2_6  = db.StringProperty(required = False)

	lfd_avg = db.StringProperty(required=False)
	source = db.StringProperty(required = False)
	dest = db.StringProperty(required = False)
	
	def getTime_22(self,key):
		return db.get(key)
		
		
class Time_23(db.Model):
   
	#day = db.StringProperty(required = False,
	#choices=set(["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]))
	day1_0  = db.StringProperty(required = False)
	day1_1  = db.StringProperty(required = False)
	day1_2  = db.StringProperty(required = False)
	day1_3  = db.StringProperty(required = False)
	day1_4  = db.StringProperty(required = False)
	day1_5  = db.StringProperty(required = False)
	day1_6  = db.StringProperty(required = False)
	
	day2_0  = db.StringProperty(required = False)
	day2_1  = db.StringProperty(required = False)
	day2_2  = db.StringProperty(required = False)
	day2_3  = db.StringProperty(required = False)
	day2_4  = db.StringProperty(required = False)
	day2_5  = db.StringProperty(required = False)
	day2_6  = db.StringProperty(required = False)

	lfd_avg = db.StringProperty(required=False)
	source = db.StringProperty(required = False)
	dest = db.StringProperty(required = False)
	
	def getTime_23(self,key):
		return db.get(key)


app = webapp2.WSGIApplication([("/newroute",NewRoute),("/welcome",MainPage),("/traffictime", TrafficAppHandler),
					("/getrouteinfo", RouteTimeHandler),("/getdigest",GetDigest),("/adddate",addDate)],
								 debug=True)



