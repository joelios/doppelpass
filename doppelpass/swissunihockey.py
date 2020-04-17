# -*- coding: utf-8 -*-
# Copyright (c) 2020, msmr.ch and contributors
# MIT License. See license.txt

from __future__ import unicode_literals
import frappe
from frappe import throw, _
import json
import base64
import requests
from requests.auth import HTTPBasicAuth
try:
	from urllib import request as http
except ImportError:
	import urllib2 as http
from datetime import datetime

def execute(host):  
	try:
		response = requests.request(method='GET', url=host)
		response.encoding = 'utf-8'
		json = response.json()
		return json
	except:
		frappe.throw("Execution of http request failed. Please check host and API token.")
        
def get_tabelle(season, league, game_class, group):
	host = "https://api-v2.swissunihockey.ch/api/rankings?season={season}&league={league}&game_class={game_class}&group={group}".format(season=season, league=league, game_class=game_class, group=group)
	results = execute(host)
	return results
	
def get_resultate(team_id, season):
	host = "https://api-v2.swissunihockey.ch/api/games?mode=team&games_per_page=100&team_id={team_id}&season={season}".format(team_id=team_id, season=season)
	results = execute(host)
	return results