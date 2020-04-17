function load_training() {
	var training = $('#training').val();
	if (training != 'leer') {
		if (training) {
			frappe.call({
				method: 'doppelpass.www.training_bearbeiten.get',
				args: {
					training: training
				},
				callback: function(r) {
					if(r.message) {
						var r = r.message;
						$('#team').val(r.team);
						$('#datum').val(r.datum);
						$('#ort').val(r.ort);
						$('#details').val(r.details);
					} 
				}
			});
		}
	} else {
		$('#team').val('leer');
		$('#datum').val('');
		$('#ort').val('');
		$('#details').val('');
		$('#training').val('leer');
	}
}

function update() {
	var team = $('#team').val();
	var datum = $('#datum').val();
	var ort = $('#ort').val();
	var details = $('#details').val();
	var training = $('#training').val();
	if ((!team)||(!datum)||(!ort)||(training == 'leer')) {
		frappe.msgprint("Bitte füllen Sie alle Pflichtfelder aus!", "Fehlende Angaben");
		return
	} else {
		frappe.call({
			method: 'doppelpass.www.training_bearbeiten.update',
			args: {
				team: team,
				datum: datum,
				ort: ort,
				details: details,
				training: training
			},
			callback: function(r) {
				if(r.message) {
					frappe.msgprint("Das Training wurde erfolgreich angepasst.", "Info");
					$('#team').val('leer');
					$('#datum').val('');
					$('#ort').val('');
					$('#details').val('');
					$('#training').val('leer');
					setTimeout(function(){ location.reload(); }, 2000);
				} 
			}
		});
	}
}

function delete_training() {
	var training = $('#training').val();
	if (training == 'leer') {
		frappe.msgprint("Bitte wählen Sie ein Training aus!", "Fehlende Angaben");
		return
	} else {
		frappe.call({
			method: 'doppelpass.www.training_bearbeiten.delete',
			args: {
				training: training
			},
			callback: function(r) {
				if(r.message) {
					frappe.msgprint("Das Training wurde erfolgreich gelöscht.", "Info");
					$('#team').val('leer');
					$('#datum').val('');
					$('#ort').val('');
					$('#details').val('');
					$('#training').val('leer');
					setTimeout(function(){ location.reload(); }, 2000);
				} 
			}
		});
	}
}