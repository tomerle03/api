#!/usr/bin/python3
import typer
import json
import datetime

from classes import *

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


# get a type like location and returns 
# the atrributes that describes the class
@app.command()
def get_attributes(api: str):
	"""
	enter a type with cappital letter
	to get q
	"""
	command = api + ".filter_types()"
	print(api + " attr are: ")
	print(list(eval(command)))

	
# get a type like location and returns all the locations
@app.command()
def get_all(api: str):
	"""
	enter type with cappital letter to get all objects
	"""
	command = api + ".get_all()"
	print(json.dumps(eval(command), indent=4))
	

# get a type like location and an id as integer 
# and return the object with that id 
@app.command()
def get_by_id(api: str, id: int):
	"""
	get type like location with cappital letter
	and an id as integer and get an object with that id
	"""
	command = api + ".getid(" + str(id) + ")"
	print(json.dumps(eval(command), indent=4))


# filter all the episodes by optional parametes 
@app.command()
def filter_episode(name=None, episode=None):
	"""
	get param for episode to filter
	run "./supercli.py get-attributes Episode"
	"""
	args = ""
	for i in list(locals().keys()):
		if eval(i) != None and i != "args":
			args += i + "=\"" + str(eval(i)) + "\","
	args = args[:-1]
	command = "Episode.filter(" + args + ")"
	print(json.dumps(eval(command), indent=4))

	
@app.command()
def filter_location(name=None, type=None, dimension=None):
	"""
	get param for location to filter
	run "./supercli.py get-attributes Location"
	"""
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
	"""
	get param for Character to filter
	run "./supercli.py get-attributes Character"
	"""
	args = ""
	for i in list(locals().keys()):
		if eval(i) != None and i != "args":
			args += i + "=\"" + str(eval(i)) + "\","

	args = args[:-1]
	command = "Character.filter(" + args + ")"
	print(json.dumps(eval(command), indent=4))

	
@app.command()
def filter_by_date(year: int, month: int, day: int, operation: str):
	"""
	enter year month and day and and > or < to get all the
	episodes before or after the input date
	"""
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
	"""
	enter location and get all the
	characters from that location
	"""
	all_characters = Character.get_all()

	all_characters = [i for a in all_characters for i in a]
	for i in all_characters:
		if i["location"]["name"] == location:
			print(json.dumps(i, indent=4))


@app.command()
def filter_by_origin(origin: str):
	"""
	enter origin and get all the
	characters from that origin
	"""
	all_characters = Character.get_all()

	all_characters = [i for a in all_characters for i in a]
	for i in all_characters:
		if i["origin"]["name"] == origin:
			print(json.dumps(i, indent=4))


@app.command()
def filter_by_season(season: int):
	"""
	enter season number and get all the
	episodes in that season
	"""
	all_episodes = Episode.get_all()
	for i in all_episodes:
		if int(i["episode"][1:3]) == season:
			print(json.dumps(i, indent=4))

			
@app.command()
def filter_by_episode(episode: int):
	"""
	enter episode and every 
	episode with that number from every season
	"""
	all_episodes = Episode.get_all()
	for i in all_episodes:
		if int(i["episode"][4:6]) == episode:
			print(json.dumps(i, indent=4))

@app.command()
def most_frequent_character(max: int=None):
	"""
	get the most frequent character in the series
	if u input --max NUMBER it will limit the output to that number
	"""
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
	del res[None]
	if max != None:
		print(dict(list(res.items())[:max]))
	else:
		print(res)


if __name__ == "__main__":
	app()
