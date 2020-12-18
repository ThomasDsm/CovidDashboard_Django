
/*
	(1,NULL),
	(2,'Flanders'),
	(3,'Wallonia'),
	(4,'Brussels');
*/
/*
	(1,NULL),
	(2,'Antwerpen'),
	(2,'WestVlaanderen'),
	(2,'OostVlaanderen'),
	(2,'Limburg'),
	(2,'VlaamsBrabant'),
	(3,'Hainaut'),
	(3,'Luxembourg'),
	(3,'Liège'),
	(3,'BrabantWallon'),
	(3,'Namur'),
	(4,'Brussels');
/* ------------------ */

// Regio's
Vlaanderen = ["vlaanderen","flanders","flandre"];
Brussel = ['brussel','brussels','bruxelles'];
Wallonie = ['wallonia','wallonie'];

// Provincies
Antwerp = ['antwerp','anvers','antwerpen'];
WVlaand = ['westvlaanderen'];
OVlaand = ['oostvlaanderen'];
Limburg = ['limburg'];
VlaamsB = ['vlaamsbrabant'];
Henegou = ['henegouwen','hainaut'];
Luxembu = ['luxemburg','luxembourg'];
Luik	= ['luik','liege'];
WaalsB  = ['waalsbrabant','brabantwallon'];
Namen	= ['namen','namur'];
// BRUSS

function clearError()
{
	$("#error").text('');
}

$(document).ready(function() {
	$("#request :input").focus(function() { clearError(); });

	$("#request").submit( function(e) 
	{
		e.preventDefault();
		clearError();
		var input = $("#request :input");
		var value = input.val();
		value = value.toLowerCase();
		
		// Change special characthers to normal char
		value = value.replace("ë","e")
		value = value.replace("è","e")
		
		// https://stackoverflow.com/questions/19156148/i-want-to-remove-double-quotes-from-a-string
		// Remove all spaces, dashes, underscores and ' 
		value = value.replace(/['-_ ]+/g, '');
		
		if (Vlaanderen.includes(value)) { console.log("Get request 'REGION':'Flanders'"); }
		else if (Brussel.includes(value))
		{
			var answer = window.prompt("Als je de regio brussel wilt bekijken, druk R.\nAls je de provincie Brussel wilt bekijken, druk P");
			if (answer == 'R')
			{
				console.log("Get request 'REGION':'Brussels'");
			}
			else if (answer == 'P')
			{
				console.log("Get request 'PROVINCE':'Brussels'");
			}
		}
		else if (Wallonie.includes(value)) 	{ console.log("Get request 'REGION':'Wallonia'"); }
		else if (Antwerp.includes(value)) 	{ console.log("Get request 'PROVINCE':'Antwerpen'"); }
		else if (WVlaand.includes(value)) 	{ console.log("Get request 'PROVINCE':'WestVlaanderen'"); }
		else if (OVlaand.includes(value)) 	{ console.log("Get request 'PROVINCE':'OostVlaanderen'"); }
		else if (Limburg.includes(value)) 	{ console.log("Get request 'PROVINCE':'Limburg'"); }
		else if (VlaamsB.includes(value)) 	{ console.log("Get request 'PROVINCE':'VlaamsBrabant'"); }
		else if (Henegou.includes(value)) 	{ console.log("Get request 'PROVINCE':'Hainaut'"); }
		else if (Luxembu.includes(value)) 	{ console.log("Get request 'PROVINCE':'Luxembourg'"); }
		else if (Luik.includes(value)) 		{ console.log("Get request 'PROVINCE':'Liège'"); }
		else if (WaalsB.includes(value)) 	{ console.log("Get request 'PROVINCE':'BrabantWallon'"); }
		else if (Namen.includes(value)) 	{ console.log("Get request 'PROVINCE':'Namur'"); }
		else
		{
			$('#error').text("De gevraagde regio of provincie is niet gevonden");
		}
	});
});
