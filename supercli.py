#!/usr/bin/python3
import itertools
import typer
import json
import datetime
import operator
import pandas as pd
from PIL import Image
from io import BytesIO
from IPython.display import display
import inspect

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


def to_table(jsn):
	"""
	this func receives a dict and prints it as a table
	"""

	for key in jsn:
		if type(jsn[key]) is dict:
			jsn[key] = jsn[key]["name"]
		elif type(jsn[key]) is list:
			jsn[key] = len(jsn[key])
		
	for v in jsn.items():
		label, num = v
		print("{:<15}| {:<10}".format(label, num))
	print("----------------------------------------")

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
	command = api + ".get_all()"
	tmp = eval(command)
	if table == None:
		print(json.dumps(tmp, indent=4))
	else:
		print("{:<15}| {:<10}".format('key','value'))
		print("{:<15}| {:<10}".format('-----','------'))
		for i in tmp:
			to_table(i)
	

# get a type like location and an id as integer 
# and return the object with that id 
@app.command()
def get_by_id(api: str, id: int, table: str=None):
	"""
	get type like location with cappital letter
	and an id as integer and get an object with that id
	"""
	command = api + ".getid(" + str(id) + ")"
	tmp = eval(command)
	if table == None:
		print(json.dumps(tmp, indent=4))
	else:
		print("{:<15}| {:<10}".format('key','value'))
		print("{:<15}| {:<10}".format('-----','------'))
		if type(tmp) is list:
			for i in tmp:
				to_table(i)
		else:
			to_table(tmp)


# filter all the episodes by optional parametes 
@app.command()
def filter_episode(name=None, episode=None, table: str=None):
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
	tmp = eval(command)
	for i in tmp:
		if table == None:
			print(json.dumps(i, indent=4))
		else:
			print("{:<15}| {:<10}".format('key','value'))
			print("{:<15}| {:<10}".format('-----','------'))
			for j in i:
				to_table(j)

	
@app.command()
def filter_location(name=None, type=None, dimension=None, table: str=None):
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
	tmp = eval(command)
	tmp = list(itertools.chain.from_iterable(tmp))
	if table == None:
		print(json.dumps(tmp, indent=4))
	else:
		print("{:<15}| {:<10}".format('key','value'))
		print("{:<15}| {:<10}".format('-----','------'))
		for i in tmp:
			to_table(i)
			
	
	
@app.command()
def filter_character(name=None, type=None, status=None, species=None, gender=None, table: str=None):
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
	tmp = eval(command)
	tmp = list(itertools.chain.from_iterable(tmp))
	if table == None:
		print(json.dumps(tmp, indent=4))
	else:
		print("{:<15}| {:<10}".format('key','value'))
		print("{:<15}| {:<10}".format('-----','------'))
		for i in tmp:
			to_table(i)

	
@app.command()
def filter_by_date(y: int, m: int, d: int, op: str, table: str=None):
	"""
	enter year month and day and and > or < to get all the
	episodes before or after the input date
	"""
	curr = datetime.datetime(year=y, month=m, day=d).date()
	all_episodes = Episode.get_all()
	for i in all_episodes:
		date = translate_date(i["air_date"])
		if op == "<":
			if date < curr:
				if table == None:
					print(json.dumps(i, indent=4))
				else:
					print("{:<15}| {:<10}".format('key','value'))
					print("{:<15}| {:<10}".format('-----','------'))
					if type(i) is list:
						for i in i:
							to_table(i)
					else:
						to_table(i)
		elif op == ">":
			if date > curr:
				if table == None:
					print(json.dumps(i, indent=4))
				else:
					print("{:<15}| {:<10}".format('key','value'))
					print("{:<15}| {:<10}".format('-----','------'))
					if type(i) is list:
						for i in i:
							to_table(i)
					else:
						to_table(i)
		else:
			print("u must enter > or <")
			break
		
@app.command()
def filter_by_location(location: str, table: str=None):
	"""
	enter location and get all the
	characters from that location
	"""
	all_characters = Character.get_all()

	for i in all_characters:
		if i["location"]["name"] == location:
			if table == None:
				print(json.dumps(i, indent=4))
			else:
				print("{:<15}| {:<10}".format('key','value'))
				print("{:<15}| {:<10}".format('-----','------'))
				if type(i) is list:
					for i in i:
						to_table(i)
				else:
					to_table(i)


@app.command()
def filter_by_origin(origin: str, table: str=None):
	"""
	enter origin and get all the
	characters from that origin
	"""
	all_characters = Character.get_all()

	for i in all_characters:
		if i["origin"]["name"] == origin:
			if table == None:
				print(json.dumps(i, indent=4))
			else:
				print("{:<15}| {:<10}".format('key','value'))
				print("{:<15}| {:<10}".format('-----','------'))
				if type(i) is list:
					for i in i:
						to_table(i)
				else:
					to_table(i)



@app.command()
def filter_by_season(season: int, table: str=None):
	"""
	enter season number and get all the
	episodes in that season
	"""
	all_episodes = Episode.get_all()
	for i in all_episodes:
		if int(i["episode"][1:3]) == season:
			if table == None:
				print(json.dumps(i, indent=4))
			else:
				print("{:<15}| {:<10}".format('key','value'))
				print("{:<15}| {:<10}".format('-----','------'))
				if type(i) is list:
					for i in i:
						to_table(i)
				else:
					to_table(i)


			
@app.command()
def filter_by_episode(episode: int, table: str=None):
	"""
	enter episode and every 
	episode with that number from every season
	"""
	all_episodes = Episode.get_all()
	for i in all_episodes:
		if int(i["episode"][4:6]) == episode:
			if table == None:
				print(json.dumps(i, indent=4))
			else:
				print("{:<15}| {:<10}".format('key','value'))
				print("{:<15}| {:<10}".format('-----','------'))
				if type(i) is list:
					for i in i:
						to_table(i)
				else:
					to_table(i)


@app.command()
def most_frequent_character(max: int=None, table: str=None):
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
		# checking for duplicates and if there are it will add the id to the name like XXXX=1234
		if names[i] in res:
			res[names[i] + "-" + str(i)] = characters[i]
		else:
			res[names[i]] = characters[i]

	# delete the first element because it has no use. the dict start at 1 not 0
	del res[None]
	if max != None:
		# ordering the dict by desc and saving the top max result to tmp
		tmp = dict(sorted(dict(list(res.items())[:max]).items(), key=operator.itemgetter(1),reverse=True))
		
		# check if user want to print a table or json
		if table == None:
			print(json.dumps(tmp, indent=4))
		else:
			print("{:<14} | {:<10}".format('key','value'))
			print("{:<14} | {:<10}".format('--------------','------'))
			if type(tmp) is list:
				for i in tmp:
					to_table(i)
			else:
				to_table(tmp)
	else:
		# ordering the dict by desc
		tmp = dict(sorted(res.items(), key=operator.itemgetter(1),reverse=True))
		if table == None:
			print(json.dumps(tmp, indent=4))
		else:
			print("{:<14} | {:<10}".format('key','value'))
			print("{:<14} | {:<10}".format('--------------','------'))
			if type(tmp) is list:
				for i in tmp:
					to_table(i)
			else:
				to_table(tmp)


@app.command()
def get_image(name=None, type=None, status=None, species=None, gender=None, id: int=None):
	"""
	this func receives filters about characters and if there is only one 
	result it will open a photo of that character
	"""
	if id != None:
		image_url = Character.getid(id)["image"]
	else:
		args = ""
		for i in list(locals().keys()):
			if eval(i) != None and i != "args":
				args += i + "=\"" + str(eval(i)) + "\","

		args = args[:-1]
		command = "Character.filter(" + args + ")"
		char_list = eval(command)[0]
		if len(char_list) != 1:
			print("ur filters got no or more then one character")
			return
		image_url = char_list[0]["image"]
	
	with Image.open(BytesIO(requests.get(image_url).content)) as im:
		im.show()
	return None

		
if __name__ == "__main__":
	app()
