#!/usr/bin/python3
import itertools
from typing import OrderedDict
from rich.console import Console
from rich.table import Table
import typer
import json
from datetime import datetime
from PIL import Image
from io import BytesIO
import requests
from api_classes import Api


app = typer.Typer()
console = Console()

def translate_date(episode_date: str) -> datetime.date:
	"""
		this func receives a date in str format like this: "December 2, 2013",
		and return a a date in dateTime format
	"""
	return datetime.strptime(episode_date, "%B %d, %Y").date()
	
		
def print_as_table(jsn):
	"""
	this func receives a dict and prints it as a table
	"""
	for key in jsn:
		if type(jsn[key]) is dict:
			jsn[key] = jsn[key]["name"]
		elif type(jsn[key]) is list:
			jsn[key] = len(jsn[key])
		
	table = Table("Name", "Item")
	for v in jsn.items():
		name, item = v
		table.add_row(name, str(item))
	console.print(table)


def req_for_all(response, table):
	if not response:
		print("you must enter episode, location or character")
		return ""
	try:
		if not table:
			print(json.dumps(response, indent=4))
		else:
			if type(response) is list:
				for i in response:
					print_as_table(i)
			else:
				print_as_table(response)
	except:
		print("you must enter episode, location or character")


def filter(api: str, name=None, episode=None, type=None, dimension=None, status=None, species=None, gender=None, table: str=None):
	args = ""
	for var in list(locals().keys()):
		if eval(var) != None and var != "args":
			args += '{0}="{1}"{2}'.format(var, str(eval(var)), ",")

	# remove last comma, not needed
	args = args[:-1]
	command = "Api.filter({0})".format(args)
	response = eval(command)
	if response == "no results found":
		print(response)
	else:
		response = list(itertools.chain.from_iterable(response))
		if not table:
			print(json.dumps(response, indent=4))
		else:
			for i in response:
				print_as_table(i)


def choose_print_type(episode, table):
	if not table:
		print(json.dumps(episode, indent=4))
	else:
		print_as_table(episode)


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
def get_all(api: str, table: str=None):
	"""
	enter type with cappital letter to get all objects
	"""
	command = Api.get_all(api)
	req_for_all(command, table)
	
	

# get a type like location and an id as integer 
# and return the object with that id 
@app.command()
def get_by_id(api: str, id: int, table: str=None):
	"""
	get type like location with cappital letter
	and an id as integer and get an object with that id
	"""
	command = Api.getid(api, id)
	req_for_all(command, table)


# filter all the episodes by optional parametes 
@app.command()
def filter_episode(name=None, episode=None, table: str=None):
	"""
	get param for episode to filter
	run "./supercli.py get-attributes Episode"
	"""
	filter("Episode", name=name, episode=episode, table=table)

	
@app.command()
def filter_location(name=None, type=None, dimension=None, table: str=None):
	"""
	get param for location to filter
	run "./supercli.py get-attributes Location"
	"""
	filter("Location", name=name, type=type, dimension=dimension, table=table)
			
	
	
@app.command()
def filter_character(name=None, type=None, status=None, species=None, gender=None, table: str=None):
	"""
	get param for Character to filter
	run "./supercli.py get-attributes Character"
	"""
	filter("Character", name=name, type=type, status=status, species=species, gender=gender, table=table)	

	
@app.command()
def filter_by_date(y: int, m: int, d: int, op: str, table: str=None):
	"""
	enter year month and day and and > or < to get all the
	episodes before or after the input date
	"""
	if op != ">" and op != "<": print("u must enter > or <"); return
	curr = datetime(year=y, month=m, day=d).date()
	all_episodes = Api.get_all("Episode")
	for episode in all_episodes:
		date = translate_date(episode["air_date"])
		if op == "<":
			if date < curr: choose_print_type(episode, table)
		elif op == ">":
			if date > curr: choose_print_type(episode, table)


# recieves filter and api to filter by any type of api
def filter_by(api: str, type_of_filter: str, user_filter, json_location: str, table: str=None):
	all_apis = Api.get_all(api)
	has_results = False
	
	for jsn in all_apis:
		if api.capitalize() == "Episode" and json_location == "season":
			if int(jsn[type_of_filter][1:3]) == user_filter:
				has_results = True
				print_as_table(jsn)
		elif api.capitalize() == "Episode" and json_location == "episode":
			if int(jsn[type_of_filter][4:6]) == user_filter:
				has_results = True
				print_as_table(jsn)
		else:
			if jsn[type_of_filter][json_location] == user_filter:
				has_results = True
				print_as_table(jsn)
	if not has_results:
		print("no results found")



@app.command()
def filter_by_location(location: str, table: str=None) -> None:
	"""
	enter location and get all the
	characters from that location
	"""
	filter_by("character", "location", json_location="name", user_filter=location, table=table)


@app.command()
def filter_by_origin(origin: str, table: str=None):
	"""
	enter origin and get all the
	characters from that origin
	"""
	filter_by(api="character", type_of_filter="origin", json_location="name", user_filter=origin, table=table)


@app.command()
def filter_by_season(season: int, table: str=None):
	"""
	enter season number and get all the
	episodes in that season
	"""
	filter_by(api="episode", type_of_filter="episode", user_filter=season, json_location="season", table=table)
	

			
@app.command()
def filter_by_episode(episode: int, table: str=None):
	"""
	enter episode and every 
	episode with that number from every season
	"""
	filter_by(api="episode", type_of_filter="episode", user_filter=episode, json_location="episode", table=table)


@app.command()
def most_frequent_character(max: int=None, table: str=None):
	"""
	get the most frequent character in the series
	if u input --max NUMBER it will limit the output to that number
	"""
	all_characters = Api.get_all("character")
	# get all characters names
	names = []
	names.append(None)
	for character in all_characters:
		names.append(character["name"])
	
	# get characters frequents apearents per id
	characters = [0] * (len(all_characters) + 1)
	for character in all_characters:
		characters[int(character["id"])] = len(character["episode"])
		
	 
	frequent_results = {}
	for position, name in enumerate(names):
		# checking for duplicates and if there are it will add the id to the name like XXXX=1234
		if name in frequent_results:
			frequent_results[name + "-" + str(position)] = characters[position]
		else:
			frequent_results[name] = characters[position]

	# delete the first element because it has no use. the dict start at 1 not 0
	del frequent_results[None]

	response = OrderedDict(frequent_results)
	if max != None:
		# ordering the dict by desc and saving the top max result to response
		response = dict(itertools.islice(response.items(), max))		
		# check if user want to print a table or json
		if not table:
			print(json.dumps(response, indent=4))
		else:
			print_as_table(response)
	else:
		# ordering the dict by desc
		if not table:
			print(json.dumps(response, indent=4))
		else:
			print_as_table(response)

    
@app.command()
def get_image(name=None, type=None, status=None, species=None, gender=None, id: int=None):
	"""
	this func receives filters about characters and if there is only one 
	result it will open a photo of that character
	"""
	if id != None:
		image_url = Api.getid("character", id)["image"]
	else:
		args = ""
		for var in list(locals().keys()):
			if eval(var) != None and var != "args":
				args += '{0}="{1}"{2}'.format(var, str(eval(var)), ",")

		args += "api=\"character\","
		args = args[:-1]
		command = "Api.filter({0})".format(args)
		char_list = eval(command)[0]
		if len(char_list) != 1 or char_list != None:
			print("ur filters got no or more then one character. num of results: " + str(len(char_list)))
			return
		print(eval(command))
		image_url = char_list[0]["image"]
	
	with Image.open(BytesIO(requests.get(image_url).content)) as im:
		im.show()
	return None

		
if __name__ == "__main__":
	app()
