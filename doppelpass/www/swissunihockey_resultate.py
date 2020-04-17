# -*- coding: utf-8 -*-
# Copyright (c) 2020, msmr.ch and Contributors
# MIT License. See license.txt

from __future__ import unicode_literals
import frappe
from frappe import _
from doppelpass.swissunihockey import get_resultate

no_cache = 1

def get_context(context):
	if frappe.session.user=='Guest':
		frappe.throw(_("You need to be logged in to access this page"), frappe.PermissionError)
	user = frappe.session.user
	#spieler = frappe.db.sql("""SELECT `name` FROM `tabTeamPlaner Mitglied` WHERE `mail` = '{user}'""".format(user=user), as_list=True)[0][0]
	#_team = frappe.db.sql("""SELECT `team` FROM `tabTeamplaner Team Verweis` WHERE `parent` = '{spieler}' LIMIT 1""".format(spieler=spieler), as_list=True)[0][0]
	#team = frappe.get_doc("TeamPlaner Team", _team)
	#context["tabelle"] = get_tabelle('2019', '6', '11', 'Gruppe+7') #get_tabelle(team.season, team.league, team.game_class, team.group)
	context["resultate"] = get_resultate('428691', '2019') #get_resultate(team.team_id, team.season)
	context["season"] = '2019' #team.season
	context["league"] = '6' #team.league
	context["game_class"] = '11' #team.game_class
	context["group"] = 'Gruppe+7' #team.group
	return context