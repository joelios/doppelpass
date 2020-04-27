# -*- coding: utf-8 -*-
# Copyright (c) 2020, msmr.ch and Contributors
# MIT License. See license.txt

from __future__ import unicode_literals
import frappe
from frappe import _
from frappe.utils.data import now_datetime

no_cache = 1

def get_context(context):
	if frappe.session.user=='Guest':
		frappe.throw(_("You need to be logged in to access this page"), frappe.PermissionError)
	
	user = frappe.get_doc("DP User", frappe.session.user)
	context["primar_bg"] = user.primar_bg
	context["sekundaer_bg"] = user.sekundaer_bg
	
	context["nachrichten"] = frappe.db.sql("""SELECT
												`tabDP Nachricht`.`datum`,
												`tabDP Nachricht`.`user`,
												`tabDP Nachricht`.`nachricht`,
												`tabDP Nachricht`.`pinned`,
												`tabDP User`.`fullname`
											FROM `tabDP Nachricht`
											INNER JOIN `tabDP User`
											ON `tabDP Nachricht`.`user` = `tabDP User`.`name`
											WHERE `tabDP Nachricht`.`pinned` = 0
											ORDER BY `tabDP Nachricht`.`datum` DESC""", as_dict=True)
											
	context["pinned_nachrichten"] = frappe.db.sql("""SELECT
												`tabDP Nachricht`.`datum`,
												`tabDP Nachricht`.`user`,
												`tabDP Nachricht`.`nachricht`,
												`tabDP Nachricht`.`pinned`,
												`tabDP User`.`fullname`
											FROM `tabDP Nachricht`
											INNER JOIN `tabDP User`
											ON `tabDP Nachricht`.`user` = `tabDP User`.`name`
											WHERE `tabDP Nachricht`.`pinned` = 1
											ORDER BY `tabDP Nachricht`.`datum` DESC""", as_dict=True)
	
	# mark all msg as read
	ungelesene_nachrichten = frappe.db.sql("""SELECT `name` FROM `tabDP Gelesen` WHERE `user` = '{user}'""".format(user=frappe.session.user), as_dict=True)
	for ungelesene_nachricht in ungelesene_nachrichten:
		frappe.db.sql("""DELETE FROM `tabDP Gelesen` WHERE `name` = '{name}'""".format(name=ungelesene_nachricht.name), as_list=True)
		frappe.db.commit()
	return context
	
@frappe.whitelist()
def add(nachricht):
	nachricht = frappe.get_doc({
		"doctype": "DP Nachricht",
		"datum": now_datetime(),
		"user": frappe.session.user,
		"nachricht": nachricht
	})
	nachricht.insert(ignore_permissions=True)
	return nachricht.name