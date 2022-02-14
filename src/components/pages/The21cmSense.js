import React from 'react';
import '../../App.css';
import { Panel } from 'rsuite';
import '../rsuite-default.css';
import { GiInfo } from "react-icons/gi";
import { Link } from 'react-router-dom';
import * as Plotly from 'plotly.js';
import '../../TestGraphDownload.js';
import { saveAs } from "file-saver";
//import { Button } from '../Button.js'; 
//import exportFromJSON from 'export-from-json';
import styled from "styled-components";
//import { Dropdown } from 'react-native-material-dropdown';
//import {CSVLink, CSVDownload} from 'react-csv';


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
    // const [UseSelectedOption, UseSetSelectedOption] = useState(null);
    // const handleChange = e => {
    //   UseSetSelectedOption(e);
    // }
// const DropDown = ({ selectedValue, options, onChange }) => {
//   return (
//     <select onChange={onChange} >
//       {
//         options.map(o => <option value={o} selected={o === selectedValue}>{o}</option>)
        
//       }
//     </select>
//   );
// }


const theme = {
  cyan: {
    default: "#F0FFFF",
    hover: "#00FFFF"
  }
};

const Button = styled.button`
  background-color: ${(props) => theme[props.theme].default};
  color: rgb(128, 0, 0);
  padding: 5px 15px;
  border-radius: 9px;
  &:hover {
    background-color: ${(props) => theme[props.theme].hover};
  }
  &:disabled {
    cursor: default;
    opacity: 0.7;
  }
`;

Button.defaultProps = {
  theme: "cyan"

};

const saveImage = () => {
  saveAs(
    "",
    "example.png"
  );
};

const saveJSON = () => {
  saveAs(
    "",
    "example.txt"
  );
};

const saveCSV = () => {
  saveAs(
    "",
    "example.csv"
  );
};

class The21cmSense extends React.Component {

  onButtonClick() {
    // Do anything
    this.popupHandler("Update");
    console.log('Button clicked');
  }
  render() {
    // const option = {
    //   "download": {
    //            "type": "string",
    //            "default": "Please Select Download Option",
    //            "dropdown": [
    //              "Image of Graph",
    //              "Parameters in JSON",
    //              "Download Graph Data in CSV"
    //            ]
    //          },
    //  }
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
              <label style={{fontWeight: 'bold', fontSize:24, fontFamily: 'Times New Roman'}}> Download Data</label>
              <br></br><br></br>
              {/* <DropDown options={option.download.dropdown}/>      */}
              {/* <Button
                onClicked={this.onButtonClick()}
              />  */}
              {/* <div>
                <button onClick={saveFile}>Download Image of Graph</button>
              </div>
              <div>
                <button onClick={saveFile}>Download Graph Data in CSV</button>
              </div> */}
        
                <Button onClick={saveJSON} style = {{fontSize:12, fontFamily: 'Rockwell', width:100}}>Download Parameters in JSON</Button>
           
                <Button onClick={saveImage} style = {{fontSize:12, fontFamily: 'Rockwell', width:100}}>Download Image of Graph</Button>
                
                <Button onClick={saveCSV} style = {{fontSize:12, fontFamily: 'Rockwell', width:100}}>Download Graph Data in CSV</Button>
             

  				    <br></br><br></br><br></br>
              
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
 