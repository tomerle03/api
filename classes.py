#!/usr/bin/python3
import typer
import json
import requests
import datetime


app = typer.Typer()

API_URL="https://rickandmortyapi.com/api/"
CHARACTER_URL=API_URL+"character/"
LOCATION_URL=API_URL+"location/"
EPISODE_URL=API_URL+"episode/"

class Character():
	def get_all():
		return Requests.get_all(CHARACTER_URL)

	def getid(id=None):
		return Requests.getid(CHARACTER_URL, id=None)

	def filter(**kwargs):
		return Requests.filter(CHARACTER_URL, **kwargs)
	

	def filter_types():
		return Requests.filter_types(CHARACTER_URL)

class Location():

	def get_all():
		return Requests.get_all(LOCATION_URL)

	def getid(id=None):
		return Requests.getid(LOCATION_URL, id=None)

	def filter(**kwargs):
		return Requests.filter(LOCATION_URL, **kwargs)
	

	def filter_types():
		return Requests.filter_types(LOCATION_URL)


class Episode():

	def get_all():
		return Requests.get_all(EPISODE_URL)

	def getid(id=None):
		return Requests.getid(EPISODE_URL, id=None)

	def filter(**kwargs):
		return Requests.filter(EPISODE_URL, **kwargs)
	

	def filter_types():
		return Requests.filter_types(EPISODE_URL)



class Requests():
	def get_all(url):
		# return json.dumps(requests.get(EPISODE_URL).json(), indent=4)\
		req = requests.get(url).json()
		res = []
		res.append(req["results"][:])
		while req["info"]["next"]:
			req = requests.get(req['info']['next']).json()
			res.append(req["results"][:])

		res = [i for a in res for i in a]
		return res
	
	def getid(url, id=None):
		if id==None:
			print("You need to pass id of character to get output.")
			print("To get list of all characters, use getall() method.")
			return
		return json.dumps(requests.get(url+str(id)).json(), indent=4)

	def filter(url, **kwargs):
		for value in kwargs:
				kwargs[value]=value+"="+kwargs[value]
		query_url='&'.join([values for values in kwargs.values()])
		final_url=url+'?'+query_url
		req = requests.get(final_url).json()
		res = []
		res.append(req["results"])
		while req["info"]["next"]:
			req = requests.get(req['info']['next']).json()
			res.append(req["results"])
		return res[0]
	

	def filter_types(url):
		temp=requests.get(url).json()
		return temp['results'][0].keys()
