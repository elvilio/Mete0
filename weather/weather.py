#!/usr/bin/env python3

import json
import requests
import matplotlib.pyplot as plt

class Weather:
	"""The heavy lifting class

	Attributes:
		__init__ 	gets the wunderground key and a tuple of the location
					(first the latitude then longitude)
		eval		takes a table of the days and returns 2 lists, 'night' 'day'
		create_days	return list of ordered days
		create_plot	creates the plot and shows it

		avewind_cal	function for wind
		temp_cal	function for temperature
		qpf_cal		function for mm of precipitations
		snow_cal	function for cm of snow
		avehumidity_cal function for average umidity
		pop_cal		function for probability of precipitations
	"""

	def __init__(self, key, loc):
		self.key = key
		self.loc = loc
		self.URL = 'http://api.wunderground.com/api/%s/forecast10day/q/%f,%f.json' % (key, loc[0], loc[1])
		f = requests.get(self.URL)
		self.forec = f.json()['forecast']['simpleforecast']['forecastday']

	def avewind_cal(self, x):
		return float(-0.0145*x**2+0.7276*x+5.8828)
	def temp_cal(self, x):
		return float(2.2e-05*x**4-0.00219*x**3+0.04662*x**2+1.116*x-9.136)
	def qpf_cal(self, x):
		return float(-0.001808*x**5+0.05123*x**4-0.4248*x**3+0.7722*x**2-1.397*x-4.585e-13)
	def snow_cal(self, x):
		return float(-0.001808*x**5+0.05123*x**4-0.4248*x**3+0.7722*x**2-1.397*x-4.585e-13)
	def avehumidity_cal(self, x):
		return float(1.376e-06*x**4-0.0003025*x**3+0.02333*x**2-0.9853*x+30)
	def pop_cal(self, x):
		return float(-5.245e-06*x**4-0.00079*x**3+0.0810*x**2-2.314*x+24.37)

	def eval(self):
		to_ret_day = [0]*10
		to_ret_night = [0]*10

		for i in range(0, 10):
			holder = self.forec[i]

			x = float(holder['avewind']['kph'])
			to_ret_day[i] += self.avewind_cal(x)

			x = float(holder['high']['celsius'])
			to_ret_day[i] += self.temp_cal(x)
			
			try:
				x = float(holder['qpf_day']['mm'])
			except:
				x = 0
			to_ret_day[i] += self.qpf_cal(x)
			
			try:
				x = float(holder['snow_day']['cm'])
			except:
				x = 0
			to_ret_day[i] += self.snow_cal(x)

			x = float(holder['avehumidity'])
			to_ret_day[i] += self.avehumidity_cal(x)

			x = float(holder['pop'])
			to_ret_day[i] += self.pop_cal(x)

		for i in range(0, 10):
			holder = self.forec[i]

			x = float(holder['avewind']['kph'])
			to_ret_night[i] += self.avewind_cal(x)

			x = float(holder['low']['celsius'])
			to_ret_night[i] += self.temp_cal(x)
			
			x = float(holder['qpf_night']['mm'])
			to_ret_night[i] += self.qpf_cal(x)

			x = float(holder['snow_night']['cm'])
			to_ret_night[i] += self.snow_cal(x)

			x = float(holder['avehumidity'])
			to_ret_night[i] += self.avehumidity_cal(x)

			x = float(holder['pop'])
			to_ret_night[i] += self.pop_cal(x)

		return to_ret_day, to_ret_night

	def create_days(self):
		date_nm = []
		for x in range(0, 10):
			date_nm.append(self.forec[x]['date']['weekday_short']+' AM')
			date_nm.append(self.forec[x]['date']['weekday_short']+' PM')
		return date_nm

	def create_plot(self, save_photo=True):
		fig, axs = plt.subplots(1, 1)

		table = []
		day, night = self.eval()
		for i in range(0, 10):
			table.append(day[i])
			table.append(night[i])

		axs.plot(range(0, 20), table)
		axs.set_xticks(range(0, 20))
		axs.set_ylim(bottom=-100, top=100)
		axs.set_xticklabels(self.create_days(), rotation=30)
		axs.set(xlabel='days', ylabel='evaluation')
		axs.grid()

		if(save_photo):
			plt.savefig('test.png', format='png', dpi=300)
		plt.show()