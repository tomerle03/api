#!/usr/bin/python3
import typer
import requests

app = typer.Typer()

API_URL="https://rickandmortyapi.com/api/"
CHARACTER_URL=API_URL+"character/"
LOCATION_URL=API_URL+"location/"
EPISODE_URL=API_URL+"episode/"

class Character():
	def get_all():
		return Requests.get_all(CHARACTER_URL)

	def getid(id):
		return Requests.getid(CHARACTER_URL, id)

	def filter(**kwargs):
		return Requests.filter(CHARACTER_URL, **kwargs)
	

	def filter_types():
		return Requests.filter_types(CHARACTER_URL)

class Location():

	def get_all():
		return Requests.get_all(LOCATION_URL)

	def getid(id):
		return Requests.getid(LOCATION_URL, id)

	def filter(**kwargs):
		return Requests.filter(LOCATION_URL, **kwargs)
	

	def filter_types():
		return Requests.filter_types(LOCATION_URL)


class Episode():

	def get_all():
		return Requests.get_all(EPISODE_URL)

	def getid(id):
		return Requests.getid(EPISODE_URL, id)

	def filter(**kwargs):
		return Requests.filter(EPISODE_URL, **kwargs)
	

	def filter_types():
		return Requests.filter_types(EPISODE_URL)



class Requests():
	def get_all(url):
		req = exec_req(url)
		res = []
		res.append(req["results"][:])
		while req["info"]["next"]:
			req = exec_req(req['info']['next'])
			res.append(req["results"][:])

		res = [i for a in res for i in a]
		return res
	
	def getid(url, id):
		if id==None:
			print("You need to pass id of character to get output.")
			print("To get list of all characters, use getall() method.")
			return
		return exec_req(url+str(id))

	def filter(url, **kwargs):
		for value in kwargs:
				kwargs[value]=value+"="+kwargs[value]
		query_url='&'.join([values for values in kwargs.values()])
		final_url=url+'?'+query_url
		req = exec_req(final_url)
		res = []
		try:
			res.append(req["results"])
			while req["info"]["next"]:
				req = exec_req(req['info']['next'])
				res.append(req["results"])
			return res
		except:
			return "no results found"
	

	def filter_types(url):
		temp = exec_req(url)
		return temp['results'][0].keys()


def exec_req(url: str):
	return requests.get(url).json()
