#!/usr/bin/python3
import typer
import json
import requests
import datetime


app = typer.Typer()

api_url="https://rickandmortyapi.com/api/"
character_url=api_url+"character/"
location_url=api_url+"location/"
episode_url=api_url+"episode/"


def translate_date(episode_date: str) -> datetime.datetime.date:
	"""
		this func receives a date in str format like this: "December 2, 2013",
		and return a a date in dateTime format
	"""
	return datetime.datetime.strptime(episode_date, "%B %d, %Y").date()


class Character():

	def get_all():
		req = requests.get(character_url).json()
		res = []
		res.append(req["results"])
		while req["info"]["next"]:
			req = requests.get(req['info']['next']).json()
			res.append(req["results"])
		res = [i for a in res for i in a]
		return res

	def get_page(number):
		return json.dumps(requests.get(character_url+'?page='+str(number)).json(), indent=4)

	def getid(id=None):
		if id==None:
			print("You need to pass id of character to get output.")
			print("To get list of all characters, use getall() method.")
			return
		return json.dumps(requests.get(character_url+str(id)).json(), indent=4)

	def filter(**kwargs):
		for value in kwargs:
				kwargs[value]=value+"="+kwargs[value]
		query_url='&'.join([values for values in kwargs.values()])
		final_url=character_url+"?"+query_url
		req = requests.get(final_url).json()
		res = []
		res.append(req["results"])
		while req["info"]["next"]:
			req = requests.get(req['info']['next']).json()
			res.append(req["results"])
		return res

	def filter_types():
		temp=requests.get(character_url).json()
		return temp['results'][0].keys()

class Location():

	def get_all():
		req = requests.get(location_url).json()
		res = []
		res.append(req["results"])
		while req["info"]["next"]:
			req = requests.get(req['info']['next']).json()
			res.append(req["results"])
		res = [i for a in res for i in a]
		return res

	def getid(id=None):
		if id==None:
			print("You need to pass id of character to get output.")
			print("To get list of all characters, use getall() method.")
			return
		return json.dumps(requests.get(location_url+str(id)).json(), indent=4)

	def filter(**kwargs):
		for value in kwargs:
				kwargs[value]=value+"="+kwargs[value]
		query_url='&'.join([values for values in kwargs.values()])
		final_url=location_url+'?'+query_url
		print(final_url)
		req = requests.get(final_url).json()
		res = []
		res.append(req["results"])
		while req["info"]["next"]:
			req = requests.get(req['info']['next']).json()
			res.append(req["results"])
		return res

	def filter_types():
		temp=requests.get(location_url).json()
		return temp['results'][0].keys()


class Episode():

	def get_all():
		# return json.dumps(requests.get(episode_url).json(), indent=4)\
		req = requests.get(episode_url).json()
		res = []
		res.append(req["results"][:])
		while req["info"]["next"]:
			req = requests.get(req['info']['next']).json()
			res.append(req["results"][:])

		res = [i for a in res for i in a]
		return res

	def getid(id=None):
		if id==None:
			print("You need to pass id of character to get output.")
			print("To get list of all characters, use getall() method.")
			return
		return json.dumps(requests.get(episode_url+str(id)).json(), indent=4)

	def filter(**kwargs):
		for value in kwargs:
				kwargs[value]=value+"="+kwargs[value]
		query_url='&'.join([values for values in kwargs.values()])
		final_url=episode_url+'?'+query_url
		req = requests.get(final_url).json()
		res = []
		res.append(req["results"])
		while req["info"]["next"]:
			req = requests.get(req['info']['next']).json()
			res.append(req["results"])
		return res[0]
	

	def filter_types():
		temp=requests.get(episode_url).json()
		return temp['results'][0].keys()

	
	

@app.command()
def get_attributes(api: str):
	command = api + ".filter_types()"
	print(type + " attr are: ")
	print(list(eval(command)))

@app.command()
def get_all(api: str):
	command = api + ".get_all()"
	print(json.dumps(eval(command), indent=4))
	

	
@app.command()
def get_by_id(api: str, id: int):
	command = api + ".getid(" + str(id) + ")"
	print(json.dumps(eval(command), indent=4))

@app.command()
def filter_episode(name=None, episode=None):
	args = ""
	for i in list(locals().keys()):
		if eval(i) != None and i != "args":
			args += i + "=\"" + str(eval(i)) + "\","

	args = args[:-1]
	command = "Episode.filter(" + args + ")"
	print(json.dumps(eval(command), indent=4))

	
@app.command()
def filter_location(name=None, type=None, dimension=None):
	args = ""
	for i in list(locals().keys()):
		if eval(i) != None and i != "args":
			args += i + "=\"" + str(eval(i)) + "\","
	args = args[:-1]
	command = "Location.filter(" + args + ")"
	print(command)
	print(json.dumps(eval(command), indent=4))
			
	
	
@app.command()
def filter_character(name=None, type=None, status=None, species=None, gender=None):
	args = ""
	for i in list(locals().keys()):
		if eval(i) != None and i != "args":
			args += i + "=\"" + str(eval(i)) + "\","

	args = args[:-1]
	command = "Character.filter(" + args + ")"
	print(json.dumps(eval(command), indent=4))

	
@app.command()
def filter_by_date(year: int, month: int, day: int, operation: str):
	curr = datetime.datetime(year=year, month=month, day=day).date()
	all_episodes = Episode.get_all()
	for i in all_episodes:
		tmp = translate_date(i["air_date"])
		if operation == "<":
			if tmp < curr:
				print(json.dumps(i, indent=4))
		elif operation == ">":
			if tmp > curr:
				print(json.dumps(i, indent=4))
		else:
			print("u must enter > or <")
		
@app.command()
def filter_by_location(location: str):
	all_characters = Character.get_all()

	all_characters = [i for a in all_characters for i in a]
	for i in all_characters:
		if i["location"]["name"] == location:
			print(json.dumps(i, indent=4))


@app.command()
def filter_by_origin(origin: str):
	all_characters = Character.get_all()

	all_characters = [i for a in all_characters for i in a]
	for i in all_characters:
		if i["origin"]["name"] == origin:
			print(json.dumps(i, indent=4))


@app.command()
def filter_by_season(season: int):
	all_episodes = Episode.get_all()
	for i in all_episodes:
		if int(i["episode"][1:3]) == season:
			print(json.dumps(i, indent=4))

			
@app.command()
def filter_by_episode(episode: int):
	all_episodes = Episode.get_all()
	for i in all_episodes:
		if int(i["episode"][4:6]) == episode:
			print(json.dumps(i, indent=4))

@app.command()
def most_frequent_character():
	all_characters = Character.get_all()
	# get all characters names
	names = []
	names.append(None)
	for c in all_characters:
		names.append(c["name"])
	
	# get characters frequents apearents per id
	characters = [0] * (len(all_characters) + 1)
	for character in all_characters:
		characters[int(character["id"])] = len(character["episode"])
		
	res = {}
	for i in range(len(names)):
		if names[i] in res:
			res[names[i] + "-" + str(i)] = characters[i]
		else:
			res[names[i]] = characters[i]
	print(res)

  
if __name__ == "__main__":
	app()
