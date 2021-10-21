import React from 'react';
import '../../App.css';


function DecodeJSON() {

//utilizes the fetch api to get data from testData.json that is located in the 
//public folder. Not sure how to fix the error in regards to having it in the data folder in src. 
//Using console.log to log the data from testData and then outputing it into a div id 
	fetch('testData.json')
	.then(response => response.json())
	.then(data => {
		console.log(data.antenna)
		document.getElementById('testAntenna').textContent = data.antenna
		console.log(data.beam)
		document.getElementById('testBeam').textContent = data.beam
		console.log(data.latitude)
		document.getElementById('testLatitude').textContent = data.latitude
	})


	return (
		<div>
		<h1>DECODE JSON to display front end</h1>
		<div id = "testAntenna"></div>
		<div id = "testBeam"></div>
		<div id = "testLatitude"></div>
	   </div> 
	   
	);


	
}


export default DecodeJSON;