import React, { useState } from 'react';
import '../../App.css';
import { Panel } from 'rsuite';
import '../rsuite-default.css';
import Select from 'react-select';
import { GiInfo } from "react-icons/gi";
import { Link } from 'react-router-dom';
//import Plot from "react-plotly.js";
// import exportFromJSON from 'export-from-json' 
//import { Dropdown } from 'react-native-material-dropdown';
//import {CSVLink, CSVDownload} from 'react-csv';

function The21cmSense(){

    //   <Plot
    //   data={[
    //     {
    //       x: [1, 2, 3],
    //       y: [2, 6, 3],
    //       type: 'scatter',
    //       mode: 'lines+markers',
    //       marker: {color: 'red'},
    //     },
    //     {type: 'bar', x: [1, 2, 3], y: [2, 5, 3]},
    //   ]}
    //   layout={ {width: 320, height: 240, title: 'A Fancy Plot'} }
    // />

    const data = [
      {
        label: "Download Image of Plot",
        
        // downloadGraph(fileName) {
        //   if(this.graphPlotted) {
        //     Plotly.downloadGraph(this.graphPlotted, {format: 'png', filename: fileName})
        //   }
      },
      {
        label: "Download JSON Data",
        //exportFromJSON({ data: JSONdata, fileName: 'download', exportType: exportFromJSON.types.xls })
      },
      {
        label:"Export Plot Details to CSV"
        //<CSVLink data={csvData} >Download me</CSVLink>
      }
    ];
    const [UseSelectedOption, UseSetSelectedOption] = useState(null);
    const handleChange = e => {
      UseSetSelectedOption(e);
    }
    return (
        <div>
            <div style={{
              display: 'inline-block', width: 700, paddingLeft: 30
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

                {UseSelectedOption
                && <div style={{ marginTop: 75, lineHeight: '25px' }}>
                 <div style={{ marginTop: 10 }}><b>Label: </b> {UseSelectedOption.label}</div>
                 {/* <Dropdown
                //   label="Download"
                //   data={data}
                //   /> */}
                  </div>
                  }
            </Panel>
            </div>

            <div className = "graph">
                <Panel shaded>
                    This is the panel for graph
                </Panel>
            </div>

        </div>

    );
}
export default The21cmSense
