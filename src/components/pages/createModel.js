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
			
      		<Panel header = 'ANTENNA' shaded style={{color: 'rgb(77, 77, 58)', fontWeight: 'bold', fontSize:21, fontFamily: 'Rockwell', paddingLeft: 20}}>
				<label> Hex Number </label>            
                <input required/>
				<br></br><br></br>
				<label> Separation </label>           
                <input required/>
				<DropDown options={option.separation.enum}/>      
  				<br></br><br></br>
			</Panel>
			<Panel header = 'BEAM' shaded style={{color: 'rgb(106, 120, 58)', fontWeight: 'bold', fontSize:21, fontFamily: 'Rockwell', paddingLeft: 20}}>
			</Panel>
			<Panel header = 'LOCATION' shaded style={{color: 'rgb(106, 120, 58)', fontWeight: 'bold', fontSize:21, fontFamily: 'Rockwell', paddingLeft: 20}}>
			</Panel>
 		</div>
  );
  }
}
	
export default CreateModel;	