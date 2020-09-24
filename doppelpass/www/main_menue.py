# -*- coding: utf-8 -*-
# Copyright (c) 2020, msmr.ch and Contributors
# MIT License. See license.txt

from __future__ import unicode_literals
import frappe
from frappe import _
from frappe.utils.data import now_datetime, nowdate
from doppelpass.swissunihockey import get_resultate, get_tabelle

no_cache = 1

def get_context(context):
	if frappe.session.user=='Guest':
		frappe.throw(_("You need to be logged in to access this page"), frappe.PermissionError)
	
	# allgemein
	user = frappe.get_doc("DP User", frappe.session.user)
	context["primar_bg"] = user.primar_bg
	context["sekundaer_bg"] = user.sekundaer_bg
	context["schriftfarbe"] = user.schriftfarbe
	
	# hauptmenue
	try:
		context["event"] = frappe.db.sql("""SELECT
												`tabDP Event`.`typ`,
												`tabDP Event`.`start`,
												`tabDP Event`.`ort`,
												`tabDP Event`.`name`
											FROM `tabDP Event`
											WHERE `start` >= '{nowdate}'
											ORDER BY `start` ASC
											LIMIT 1""".format(nowdate=now_datetime()), as_dict=True)[0]
		event = frappe.get_doc("DP Event", context["event"]["name"])
		context["anwesend"] = False
		context["anzahl"] = len(event.anmeldungen)
		for teilnehmer in event.anmeldungen:
			if frappe.session.user == teilnehmer.user:
				context["anwesend"] = teilnehmer.name
	except:
		context["event"] = None
		context["anwesend"] = False
		
	# swissunihockey
	context["tabelle"] = get_tabelle('2020', '5', '11', 'Gruppe+5') #get_tabelle(team.season, team.league, team.game_class, team.group)
	context["resultate"] = get_resultate('428691', '2020') #get_resultate(team.team_id, team.season)
	context["season"] = '2020' #team.season
	context["league"] = '5' #team.league
	context["game_class"] = '11' #team.game_class
	context["group"] = 'Gruppe+5' #team.group
	
	# topscorer und präsenz
	users = frappe.db.sql("""SELECT `name`, `fullname` FROM `tabDP User`""", as_dict=True)
	context["prasenz"] = []
	for user in users:
		user_dict = {}
		user_dict["user"] = user.fullname
		
		# präsenz
		try:
			user_dict["anzahl"] = int(frappe.db.sql("""SELECT COUNT(`name`) FROM `tabDP Event` WHERE `start` < '{nowdate}'""".format(nowdate=nowdate()), as_list=True)[0][0])
		except:
			user_dict["anzahl"] = 0
		
		try:
			user_dict["anwesend"] = int(frappe.db.sql("""SELECT COUNT(`name`)
													FROM `tabTeilnehmer`
													WHERE `user` = '{user}'
													AND `parent` IN (
													SELECT `name` FROM `tabDP Event` WHERE `start` < '{nowdate}'
													)""".format(nowdate=nowdate(), user=user.name), as_list=True)[0][0])
		except:
			user_dict["anwesend"] = 0
			
		try:
			user_dict["prozent"] = round((100 / user_dict["anzahl"]) * user_dict["anwesend"], 2)
		except:
			user_dict["prozent"] = 0
			
		
		
		# skorerpunkte
		user_data = frappe.get_doc("DP User", user.name)
		user_dict["tore"] = user_data.tore
		user_dict["assists"] = user_data.assists
		user_dict["total_punkte"] = user_data.tore + user_data.assists
		
		context["prasenz"].append(user_dict)
		
	# Kasse
	context["saldo"] = frappe.db.get_single_value('DP Kasse', 'saldo')
	context["bezahlt"] = frappe.db.get_single_value('DP Kasse', 'bezahlt')
	context["offen"] = frappe.db.get_single_value('DP Kasse', 'offen')
	context["bussen"] = frappe.db.sql("""SELECT
											`tabDP Bussen`.`betrag`,
											`tabDP User`.`fullname`,
											`tabDP Bussen`.`begruendung`
										FROM `tabDP Bussen`
										INNER JOIN `tabDP User`
										ON `tabDP Bussen`.`user` = `tabDP User`.`name`""", as_dict=True)
										
	# profil
	context["user"] = frappe.get_doc("DP User", frappe.session.user)
	context["strasse"] = context["user"].strasse
	context["ort"] = context["user"].ort
	context["geburtsdatum"] = context["user"].geburtsdatum
	context["telefon"] = context["user"].telefon
	context["plz"] = context["user"].plz
	context["fullname"] = context["user"].fullname
	
	# Kalender
	context["events_in_zukunft"] = frappe.db.sql("""SELECT
													`tabDP Event`.`typ`,
													`tabDP Event`.`start`,
													`tabDP Event`.`ort`,
													`tabDP Event`.`name`,
													`tabDP Event`.`gegner`,
													`tabDP Event`.`details`
												FROM `tabDP Event`
												WHERE DATE(`start`) > '{nowdate}'
												ORDER BY `start` ASC""".format(nowdate=nowdate()), as_dict=True)
	context["details_zu_events"] = {}
	for _event in context["events_in_zukunft"]:
		_event = frappe.get_doc("DP Event", _event.name)
		context["details_zu_events"][_event.name] = {}
		context["details_zu_events"][_event.name]["anwesend"] = False
		context["details_zu_events"][_event.name]["anzahl"] = len(_event.anmeldungen)
		for teilnehmer in _event.anmeldungen:
			if frappe.session.user == teilnehmer.user:
				context["details_zu_events"][_event.name]["anwesend"] = teilnehmer.name
				
	# Team
	context["users"] = frappe.db.sql("""SELECT * FROM `tabDP User` ORDER BY `fullname` ASC""", as_dict=True)
	
	return context
	
@frappe.whitelist()
def abmelden(ref):
	frappe.db.sql("""DELETE FROM `tabTeilnehmer` WHERE `name` = '{ref}'""".format(ref=ref), as_list=True)
	return True
	
@frappe.whitelist()
def anmelden(event):
	event = frappe.get_doc("DP Event", event)
	row = event.append('anmeldungen', {})
	row.user = frappe.session.user
	event.save(ignore_permissions=True)
	return True
	
@frappe.whitelist()
def show_teilnehmer(event):
	event = frappe.get_doc("DP Event", event)
	anmeldungen = []
	for anmeldung in event.anmeldungen:
		user = frappe.get_doc("DP User", anmeldung.user)
		anmeldungen.append([user.fullname, user.position])
	return anmeldungen
	
@frappe.whitelist()
def primebackground_change(color):
	frappe.db.sql("""UPDATE `tabDP User` SET `primar_bg` = '{color}' WHERE `name` = '{user}'""".format(color=color, user=frappe.session.user), as_list=True)
	frappe.db.commit()
	return 'ok'
	
@frappe.whitelist()
def secbackground_change(color):
	frappe.db.sql("""UPDATE `tabDP User` SET `sekundaer_bg` = '{color}' WHERE `name` = '{user}'""".format(color=color, user=frappe.session.user), as_list=True)
	frappe.db.commit()
	return 'ok'
	
@frappe.whitelist()
def schriftfarbe_change(color):
	frappe.db.sql("""UPDATE `tabDP User` SET `schriftfarbe` = '{color}' WHERE `name` = '{user}'""".format(color=color, user=frappe.session.user), as_list=True)
	frappe.db.commit()
	return 'ok'
	
@frappe.whitelist()
def team_ansicht_change(team_ansicht):
	frappe.db.sql("""UPDATE `tabDP User` SET `team_ansicht` = '{team_ansicht}' WHERE `name` = '{user}'""".format(team_ansicht=team_ansicht, user=frappe.session.user), as_list=True)
	frappe.db.commit()
	return 'ok'
	
@frappe.whitelist()
def update_kontakt(fullname, plz, telefon, geburtsdatum, ort, strasse):
	frappe.db.sql("""UPDATE `tabDP User` SET `fullname` = '{fullname}',
												`plz` = '{plz}',
												`telefon` = '{telefon}',
												`geburtsdatum` = '{geburtsdatum}',
												`ort` = '{ort}',
												`strasse` = '{strasse}'
					WHERE `name` = '{user}'""".format(fullname=fullname, plz=plz, telefon=telefon, geburtsdatum=geburtsdatum, ort=ort, strasse=strasse, user=frappe.session.user), as_list=True)
	frappe.db.commit()
	return 'ok'