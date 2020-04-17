function add() {
	var team = $('#team').val();
	var datum = $('#datum').val();
	var ort = $('#ort').val();
	var details = $('#details').val();
	if ((!team)||(!datum)||(!ort)) {
		frappe.msgprint("Bitte füllen Sie alle Pflichtfelder aus!", "Fehlende Angaben");
		return
	} else {
		frappe.call({
			method: 'doppelpass.www.training_add.add',
			args: {
				team: team,
				datum: datum,
				ort: ort,
				details: details
			},
			callback: function(r) {
				if(r.message) {
					frappe.msgprint("Das Training mit der ID '" + r.message + "' wurde erfolgreich erfasst.<br>Sie werden gleich weitergeleitet.", "Info");
					setTimeout(function(){ window.location='/submenu_training_konfiguration'; }, 3000);
				} 
			}
		});
	}
}