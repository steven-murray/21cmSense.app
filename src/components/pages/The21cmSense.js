import React, { useState } from 'react';
import '../../App.css';
import { Panel } from 'rsuite';
import '../rsuite-default.css';
import Select from 'react-select';
import "react-plotly.js";
import { GiInfo } from "react-icons/gi";
import { Link } from 'react-router-dom';
// import exportFromJSON from 'export-from-json' 
// import { Dropdown } from 'react-native-material-dropdown';

function The21cmSense(){

  var img_jpg= d3.select('#jpg-export');

    // Plotting the Graph

    var trace={x:[3,9,8,10,4,6,5],y:[5,7,6,7,8,9,8],type:"scatter"};
    var trace1={x:[3,4,1,6,8,9,5],y:[4,2,5,2,1,7,3],type:"scatter"};
    var dataPlot = [trace,trace1];
    var layout = {title : "Simple JavaScript Graph"};
    Plotly.newPlot(
      'plotly_div',
      dataPlot,
      layout)

    // static image in jpg format

    .then(
        function(gd)
        {
          Plotly.toImage(gd,{height:300,width:300})
            .then(
                function(url)
            {
                img_jpg.attr("src", url);
            }
            )
        });
    <img id="jpg-export"></img>
    const data = [
      {
        value: "Download Image of Plot",
        
        downloadGraph(fileName) {
          if(this.graphPlotted) {
            Plot.downloadImage(this.graphPlotted, {format: 'png', filename: fileName})
          }
      }
      },
      {
        value: "Download JSON Data",
        //exportFromJSON({ data: JSONdata, fileName: 'download', exportType: exportFromJSON.types.xls })
      },
      {
        value:"Export Plot Details to CSV"
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
             <div style={{ marginTop: 10 }}><b>Label: </b> {UseSelectedOption.value}</div>
            {/* <Dropdown 
              label="Download"
              data={data}
              /> */}
              </div>}
        </Panel>
        </div>

    );
}
export default The21cmSense
