import React from 'react';
import '../../App.css';
import { Panel } from 'rsuite';
import '../rsuite-default.css';
import { GiInfo } from "react-icons/gi";

function the21cmSense(){
    return (
        <div style={{
      display: 'block', width: 700, paddingLeft: 30 
    }}>
      <br></br>
      <Panel  shaded >
		<label style={{fontWeight: 'bold', fontSize:24, fontFamily: 'Times New Roman'}}> Model <GiInfo title = "create,edit, or delete"/> </label>
		
		<button style={{ float: 'right', fontWeight: 'bold', fontSize:18}} title="New Model"> + </button> 
		<br></br><br></br>
        No models created yet. Please click "New Model"
      </Panel>

    </div>
    );
}
export default the21cmSense;