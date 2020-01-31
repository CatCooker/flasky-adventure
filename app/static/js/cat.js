// BUDDY!

const pupils = document.querySelectorAll('.pupil');
let trackingArea = document.querySelector('body');
const buddy = document.querySelector('.buddy');
const eyeTrigger = document.querySelectorAll('.switch');

const eyeTracking = (e) => {
	var x = event.clientX * 100 / window.innerWidth + "%";
	var y = event.clientY * 100 / window.innerHeight + "%";

	pupils.forEach(pupil => {
		pupil.style.left = x;
		pupil.style.top = y;
		pupil.style.transform = `translate(-${x}, -${y})`;
	});
};

trackingArea.addEventListener('mousemove', eyeTracking);

eyeTrigger.forEach(trigger => {
	trigger.addEventListener('mouseenter', e => {
			buddy.classList.add('hunter');
	});

	trigger.addEventListener('mouseleave', e => {
			buddy.classList.remove('hunter');
	});
});


// SNOW! based on kurisu brooks' snow.js

// Settings
// let snowMax = 100; SET IN THE TOGGLE.
const snowColor = ["#DDD", "#EEE"];
const snowEntity = "&#x2022;";
const snowSpeed = 0.3;
const snowMinSize = 8;
const snowMaxSize = 40;
const snowRefresh = 10;

let snow = [],
	pos = [],
	coords = [],
	lefr = [],
	marginBottom,
	marginRight;

const randomise = range => {
	rand = Math.floor(range * Math.random());
	return rand;
}
const initSnow = () => {

	if(snowMax > 0) {

	const globeypls = document.querySelector('.globe-inner');
	for (i = 0; i <= snowMax; i++) {
		const flake = document.createElement('span');
		flake.innerHTML = `${snowEntity}`;
		flake.classList.add(`flake`, `flake${i}`);
		globeypls.appendChild(flake);
	}

	let snowSize = snowMaxSize - snowMinSize;
	marginBottom = document.body.scrollHeight - 5;
	marginRight = document.body.clientWidth - 15;
	for (i = 0; i <= snowMax; i++) {
		coords[i] = 0;
		lefr[i] = Math.random() * 15;
		pos[i] = 0.03 + Math.random() / 10;
		snow[i] = document.querySelector(".flake" + i);
		snow[i].style.fontFamily = "inherit";
		snow[i].size = randomise(snowSize) + snowMinSize;
		snow[i].style.fontSize = snow[i].size + "px";
		snow[i].style.color = snowColor[randomise(snowColor.length)];
		snow[i].style.zIndex = Math.round(Math.random() * 10);
		snow[i].sink = snowSpeed * snow[i].size / 5;
		snow[i].posX = randomise(marginRight - snow[i].size);
		snow[i].posY = randomise(2 * marginBottom - marginBottom - 2 * snow[i].size);
		snow[i].style.left = snow[i].posX + "px";
		snow[i].style.top = snow[i].posY + "px";
	}
	moveSnow();
	}
}
const resize = () => {
	marginBottom = document.body.scrollHeight - 5;
	marginRight = document.body.clientWidth - 15;
}

const moveSnow = () => {
	if(snowMax > 0) {
	for (i = 0; i <= snowMax; i++) {
		coords[i] += pos[i];
		snow[i].posY += snow[i].sink;
		snow[i].style.left = snow[i].posX + lefr[i] * Math.sin(coords[i]) + "px";
		snow[i].style.top = snow[i].posY + "px";

		if (snow[i].posY >= marginBottom - 2 * snow[i].size || parseInt(snow[i].style.left) > (marginRight - 3 * lefr[i])) {
			snow[i].posX = randomise(marginRight - snow[i].size);
			snow[i].posY = 0;
		}
	}

	setTimeout("moveSnow()", snowRefresh);
}
}


// GLOBE CONTROL

const checkbox = document.querySelector("input[name=globe-switch]");
const globe = document.querySelector('.globe');

checkbox.addEventListener( 'change', function() {
    if(this.checked) {
			snowMax = 100;

			// setTimeout(() => initSnow(), 1000);
			initSnow();
			globe.classList.add('frosty');
			// Maybe add a class that then does the fade up animation on the flakes?

			// Remove big eyes when clicking (mobile ux)
			buddy.classList.remove('hunter');

			// Remove tracking?
			// trackingArea.removeEventListener('mousemove', addTracking);

			// initSnow();
    } else {
			globe.classList.remove('frosty');
			// Reset everything and remove all of the flakes.
			// [TO DO] - Error on forloop that needs sorting.
			snowMax = 0;
			snow = [];
			pos = [];
			coords = [];
			lefr = [];
			let flakeQty = document.querySelectorAll('.flake');
			flakeQty.forEach(flake => {
				flake.remove();
			});
		}
});
