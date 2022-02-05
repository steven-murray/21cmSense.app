import React, { useState } from 'react';
import '../../App.css';
import { Panel } from 'rsuite';
import '../rsuite-default.css';
import Select from 'react-select';
// import Plot from "react-plotly.js";
import { GiInfo } from "react-icons/gi";
import { Link } from 'react-router-dom';

function The21cmSense(){
    const data = [
      {
        label: "Download Image of Plot",
      //   downloadGraph(fileName) {
      //     if(this.graphPlotted) {
      //       Plot.downloadImage(this.graphPlotted, {format: 'png', filename: fileName})
      //     }
      // }
    },
      {
        label: "Download JSON Data"
      },
      {
        label:"Export Plot Details to CSV"
      }
    ];
    const [UseSelectedOption, UseSetSelectedOption] = useState(null);
    const handleChange = e => {
      UseSetSelectedOption(e);
    }
    return (
        <div style={{
          display: 'block', width: 700, paddingLeft: 30 
        }}>
          <br></br>
          <Panel  shaded >
          <label style={{fontWeight: 'bold', fontSize:24, fontFamily: 'Times New Roman'}}> Model <GiInfo title = "create,edit, or delete"/> </label>
          <Link to='/createModel'>
			    <button style={{ float: 'right', fontWeight: 'bold', fontSize:18}} title="New Model" > + </button> 
		    </Link>
        <br></br><br></br>
            No models created yet. Please click "New Model"
          </Panel>
          <br></br>
          <Panel  shaded >
          <label style={{fontWeight: 'bold', fontSize:24, fontFamily: 'Times New Roman'}}> Download </label>
            <Select
              placeholder="Select Options"
              value={UseSelectedOption}
              options={data}
              onChange={handleChange}
            />
            {UseSelectedOption && <div style={{ marginTop: 75, lineHeight: '25px' }}>
             <div style={{ marginTop: 10 }}><b>Label: </b> {UseSelectedOption.label}</div>
            </div>}
        </Panel>
        </div>

    );
}
export default The21cmSense