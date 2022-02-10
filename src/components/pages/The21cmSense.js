import React from 'react';
import '../../App.css';
import { Panel } from 'rsuite';
import '../rsuite-default.css';
import { GiInfo } from "react-icons/gi";
import { Link } from 'react-router-dom';
import * as Plotly from 'plotly.js';
import '../../TestGraphDownload.js';
// import exportFromJSON from 'export-from-json' 
//import { Dropdown } from 'react-native-material-dropdown';
//import {CSVLink, CSVDownload} from 'react-csv';

const imagePlot = [
  Plotly.downloadImage('TestGraphDownload.js', {format: 'png', width: 800, height: 600, filename: 'newplot'})
]

// const data = [
//   {
//     label: "Download Image of Plot",
    
//     // downloadGraph(fileName) {
//     //   if(this.graphPlotted) {
//     //     Plotly.downloadGraph(this.graphPlotted, {format: 'png', filename: fileName})
//     //   }
//   },
//   {
//     label: "Download JSON Data",
//     //exportFromJSON({ data: JSONdata, fileName: 'download', exportType: exportFromJSON.types.xls })
//   },
//   {
//     label:"Export Plot Details to CSV"
//     //<CSVLink data={csvData} >Download me</CSVLink>
//   }
// ];


const DropDown = ({ selectedValue, options, onChange }) => {
  return (
    <select onChange={onChange} >
      {
        options.map(o => <data value={o} selected={o === selectedValue}>{o}</data>)
        
      }
    </select>
  );
}

class The21cmSense extends React.Component{
    render() {
      const data = [ {
        label: "Download Image Of Plot",
        imagePlot
      }, {
        label: "Download JSON Data",
      }, {
        label: "Export Plot Details to CSV"
      }
      ]

      
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

                  <DropDown options={data.separation.enum}/>
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
}
export default The21cmSense
