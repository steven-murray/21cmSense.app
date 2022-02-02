import '../../App.css';
import React from 'react';
import { Panel } from 'rsuite';

class CreateModel extends React.Component {

render() {
     return (
		<div style={{display: 'block', width: 700, paddingLeft: 30 }}>
			<br></br>
      		<Panel  shaded >
				<label style={{fontWeight: 'bold', fontSize:21, fontFamily: 'Rockwell'}}> ANTENNA </label>
			</Panel>
 		</div>
       
  );
  }
}
	
export default CreateModel;	