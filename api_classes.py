#!/usr/bin/python3
import requests
from requests.exceptions import MissingSchema

API_URL="https://rickandmortyapi.com/api/"
CHARACTER_URL=API_URL+"character/"
LOCATION_URL=API_URL+"location/"
EPISODE_URL=API_URL+"episode/"


def get_url(api: str):
	match(api.capitalize()):
		case "Episode":
			return EPISODE_URL
		case "Location":
			return LOCATION_URL
		case "Character":
			return CHARACTER_URL
	return "api error, " + api + " does not exist"


class Api():
	def get_all(api: str):
		return Requests.get_all(get_url(api))

	def getid(api, id):
		return Requests.getid(get_url(api), id)

	def filter(**kwargs):
		return Requests.filter(get_url(kwargs["api"]), **kwargs)
	
	def filter_types(api):
		return Requests.filter_types(get_url(api))


class Requests():
	def get_all(url):
		try:
			request = exec_req(url)
		except MissingSchema:
			return
		res = []
		res.append(request["results"][:])
		while request["info"]["next"]:
			request = exec_req(request['info']['next'])
			res.append(request["results"][:])
			
		# [[], [], [], []] -> []
		res = [i for a in res for i in a]
		return res
	
	def getid(url, id):
		if id==None:
			print("You need to pass id to get output.")
			print("To get list of all characters, use getall() method.")
			return
		try:
			request = exec_req(url+str(id))
		except MissingSchema:
			return
		return request


	def filter(url, **kwargs):
		for value in kwargs:
				kwargs[value]=value+"="+kwargs[value]
		query_url='&'.join([values for values in kwargs.values()])
		final_url=url+'?'+query_url
		request = exec_req(final_url)
		res = []
		try:
			res.append(request["results"])
			while request["info"]["next"]:
				request = exec_req(request['info']['next'])
				res.append(request["results"])
			return res
		except:
			return "no results found"
	

	def filter_types(url):
		temp = exec_req(url)
		return temp['results'][0].keys()


def exec_req(url: str):
	return requests.get(url).json()
