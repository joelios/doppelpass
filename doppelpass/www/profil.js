/* function primebackground_change() {
	new_bg = $('#pimebackgroundcolor').val();
	if ((!new_bg)) {
		frappe.msgprint("Bitte tragen Sie eine Farbe ein!", "Fehlende Angaben");
		return
	} else {
		frappe.call({
			method: 'doppelpass.www.profil.primebackground_change',
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
			method: 'doppelpass.www.profil.secbackground_change',
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
			method: 'doppelpass.www.profil.primebackground_change',
			args: {
				color: new_primar
			},
			callback: function(r) {
				if(r.message) {
					frappe.call({
						method: 'doppelpass.www.profil.secbackground_change',
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
} */