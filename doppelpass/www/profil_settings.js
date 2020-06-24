function primebackground_change() {
	new_bg = $('#pimebackgroundcolor').val();
	if ((!new_bg)) {
		frappe.msgprint("Bitte tragen Sie eine Farbe ein!", "Fehlende Angaben");
		return
	} else {
		frappe.call({
			method: 'doppelpass.www.profil_settings.primebackground_change',
			args: {
				color: new_bg
			},
			callback: function(r) {
				if(r.message) {
					location.reload();
				} 
			}
		});
	}
}

function secbackground_change() {
	new_bg = $('#secbackgroundcolor').val();
	if ((!new_bg)) {
		frappe.msgprint("Bitte tragen Sie eine Farbe ein!", "Fehlende Angaben");
		return
	} else {
		frappe.call({
			method: 'doppelpass.www.profil_settings.secbackground_change',
			args: {
				color: new_bg
			},
			callback: function(r) {
				if(r.message) {
					location.reload();
				} 
			}
		});
	}
}

function reset_colors() {
	var new_primar = '#47aff8';
	var new_sekundaer = '#3c5c73';
	frappe.call({
		method: 'doppelpass.www.profil_settings.primebackground_change',
		args: {
			color: new_primar
		},
		callback: function(r) {
			if(r.message) {
				frappe.call({
					method: 'doppelpass.www.profil_settings.secbackground_change',
					args: {
						color: new_sekundaer
					},
					callback: function(r) {
						if(r.message) {
							location.reload();
						} 
					}
				});
			} 
		}
	});
}

function team_ansicht_change() {
	new_team_ansicht = $('#team_ansicht').val();
	console.log(new_team_ansicht);
	if ((!new_team_ansicht)) {
		frappe.msgprint("Bitte tragen Sie eine Team Ansicht ein!", "Fehlende Angaben");
		return
	} else {
		frappe.call({
			method: 'doppelpass.www.profil_settings.team_ansicht_change',
			args: {
				team_ansicht: new_team_ansicht
			},
			callback: function(r) {
				if(r.message) {
					location.reload();
				} 
			}
		});
	}
}

function update_kontakt() {
	var fullname = $('#fullname').val();
	var plz = $('#plz').val();
	var telefon = $('#telefon').val();
	var geburtsdatum = $('#geburtsdatum').val();
	var ort = $('#ort').val();
	var strasse =$('#strasse').val();
	frappe.call({
		method: 'doppelpass.www.profil_settings.update_kontakt',
		args: {
			fullname: fullname,
			plz: plz,
			telefon: telefon,
			geburtsdatum: geburtsdatum,
			ort: ort,
			strasse: strasse
		},
		callback: function(r) {
			if(r.message) {
				location.reload();
			} 
		}
	});
}