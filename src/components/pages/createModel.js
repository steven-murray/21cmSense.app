import '../../App.css';
import React from 'react';
import { Panel } from 'rsuite';

class CreateModel extends React.Component {

render() {
     return (
		<div style={{display: 'block', width: 700, paddingLeft: 30 }}>
			<br></br>
      		<Panel header = 'ANTENNA' shaded style={{color: 'rgb(106, 120, 58)', fontWeight: 'bold', fontSize:21, fontFamily: 'Rockwell', paddingLeft: 30}}>
			</Panel>
 		</div>
       
  );
  }
}
	
export default CreateModel;	