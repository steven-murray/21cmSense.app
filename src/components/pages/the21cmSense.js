import React from 'react';
import '../../App.css';
import { Panel } from 'rsuite';
import '../rsuite-default.css';

function the21cmSense(){
    return (
        <div style={{
      display: 'block', width: 700, paddingLeft: 30 
    }}>
      <br></br>
      <Panel  shaded >
		<label> Model </label>
		<button style={{ float: 'right'}}> + </button> 
		<br></br><br></br>
        No models created yet. Please click "New Model"
      </Panel>

    </div>
    );
}
export default the21cmSense;