# -*- coding: utf-8 -*-
# Copyright (c) 2020, msmr.ch and Contributors
# MIT License. See license.txt

from __future__ import unicode_literals
import frappe
from frappe import _
from frappe.utils.data import nowdate

no_cache = 1

def get_context(context):
	if frappe.session.user=='Guest':
		frappe.throw(_("You need to be logged in to access this page"), frappe.PermissionError)
	
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
			user_dict["prozent"] = (100 / user_dict["anzahl"]) * user_dict["anwesend"]
		except:
			user_dict["prozent"] = 0
			
		
		
		# skorerpunkte
		user_data = frappe.get_doc("DP User", user.name)
		user_dict["tore"] = user_data.tore
		user_dict["assists"] = user_data.assists
		user_dict["total_punkte"] = user_data.tore + user_data.assists
		
		context["prasenz"].append(user_dict)
		
	return context