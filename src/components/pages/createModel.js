import '../../App.css';
import React from 'react';
import { Panel } from 'rsuite';

const DropDown = ({ selectedValue, options, onChange }) => {
  return (
    <select onChange={onChange} >
      {
        options.map(o => <option value={o} selected={o === selectedValue}>{o}</option>)
        
      }
    </select>
  );
}

class CreateModel extends React.Component {


render() {
		const option = {
						 "separation": {
							        "type": "string",
							        "default": "m",
							        "enum": [
							          "m",
							          "s"
							        ]
							      }
						}
     return (
			<div style={{display: 'block', width: 900, paddingLeft: 30 }}>
			<br></br>
			
      		<Panel header = 'ANTENNA' shaded style={{color: 'rgb(77, 77, 58)', fontSize:21, fontFamily: 'Rockwell', paddingLeft: 20}}>
				<label> Hex Number </label>            
                <input type = {"number"} min={3}required/>
				<br></br><br></br>
				<label> Separation </label>           
                <input type = {"number"} min={0}required/>
				<DropDown options={option.separation.enum}/>      
  				<br></br><br></br>
				<label> Distance </label>           
                <input type = {"number"} min={0}required/>
				<DropDown options={option.separation.enum}/>      
  				<br></br><br></br>
			</Panel>
			<Panel header = 'BEAM' shaded  style={{color: 'rgb(77, 77, 58)', fontSize:21, fontFamily: 'Rockwell', paddingLeft: 20}}>
				<label> Dish Size </label>           
                <input type = {"number"} min={0}required/>
				<DropDown options={option.separation.enum}/>      
  				<br></br><br></br>
			</Panel>
			<Panel header = 'LOCATION' shaded style={{color: 'rgb(77, 77, 58)', fontSize:21, fontFamily: 'Rockwell', paddingLeft: 20}}>
				<label> Latitude </label> 
				<input type = {"number"} min={-180} max = {180} required/>
				<DropDown options={option.separation.enum}/>      
  				<br></br><br></br>
			</Panel>
			<br></br><br></br>
			<label style = {{color: 'rgb(128, 0, 0)', fontSize:18, fontFamily: 'Rockwell', width:180}}> Model Name </label>
			<input type = {"text"} required/>
 		</div>
  );
  }
}
	
export default CreateModel;	