import '../../App.css';
import React from 'react';
import { Panel } from 'rsuite';

class CreateModel extends React.Component {

render() {
     return (
		<div style={{display: 'block', width: 700, paddingLeft: 30 }}>
			<br></br>
      		<Panel header = 'ANTENNA' shaded style={{color: 'rgb(106, 120, 58)', fontWeight: 'bold', fontSize:21, fontFamily: 'Rockwell', paddingLeft: 20}}>
				<label> Hex Number </label>            
                <input required/>
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