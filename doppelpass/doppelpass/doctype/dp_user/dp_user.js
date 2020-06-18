// Copyright (c) 2020, msmr.ch and contributors
// For license information, please see license.txt

frappe.ui.form.on('DP User', {
	refresh: function(frm) {
		frm.add_custom_button(__("Spieler zu allen künftigen Events hinzufügen"), function() {
            hinzufuegen(frm);
        });
	}
});


function hinzufuegen(frm) {
	frappe.call({
       method: "doppelpass.doppelpass.doctype.dp_event.dp_event.add_spieler",
       args: {
            "spieler": frm.doc.name,
            "fullname": frm.doc.fullname
       },
       callback: function(response) {
            var antwort = response.message;
            if (antwort) {
               if (antwort == 'ok') {
				   frappe.msgprint("Der Spieler wurde zu allen Events hinzugefügt.");
			   } else {
				   frappe.msgprint(String(antwort));
			   }
            } else {
               frappe.msgprint("error");
            }
       }
    });
}