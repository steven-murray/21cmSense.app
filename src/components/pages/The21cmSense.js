import React from 'react';
import '../../App.css';
import { Panel } from 'rsuite';
import '../rsuite-default.css';
import { GiInfo } from "react-icons/gi";
import { Link } from 'react-router-dom';
import '../../TestGraphDownload.js';
import { saveAs } from "file-saver";
import styled from "styled-components";



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
    // img_png.attr("src", url),
    // Plotly.toImage(gd,{format:'png',height:400,width:400}),
    "example.png"
  );
};

const saveJSON = () => {
  saveAs(
    "",
    "example.json"
  );
};

const saveCSV = () => {
  saveAs(
    "",
    "example.csv"
  );
};
	
class The21cmSense extends React.Component {
	constructor(props) {
	    super(props);
		
	    this.state = {
	     	modelName: '',
		  	HexNumber: '',
		  	Separation: '',
		  	Distance: '',
		 	DishSize: '',
		  	Frequency: '',
		  	Latitude: '',
		  	SeperationUnits: '',
			DistanceUnits: '',
			FrequencyUnits: '',
			LatitudeUnits: '',
			localStoragePairs: []
	    }
	  }
	  
	  componentDidMount() {
	    this.getExistingArray();		
	  }
	
	  getExistingArray() {
	
	    for (var i = 0; i < localStorage.length; i++) {
	
	      var key = localStorage.key(i);
	      var value = localStorage.getItem(key);
	
	      var updatedLocalStoragePairs = this.state.localStoragePairs;
	      updatedLocalStoragePairs.push({ 'keyName': key, 'valueName': value });
	
	      this.setState({ localStoragePairs: updatedLocalStoragePairs });
	    }
	    console.log("complete localStoragePairs:", this.state.localStoragePairs);
	
	    if (localStorage.getItem('inputs')) {
	      var storedInputs = localStorage.getItem('inputs');
	      this.setState({ inputs: storedInputs }, function () { console.log("from localStorage We got:", this.state.inputs); });
	    }
	  }


  render() {
	const {  modelName } = (this.props.location && this.props.location.state) || {};
	localStorage.setItem(modelName, JSON.stringify((this.props.location && this.props.location.state) || {}));
		
	const LocalSotrageContent = this.state.localStoragePairs.map((value, index) => {
      return <tr key={index}> <td>{value.keyName}</td> </tr>
    });
    return (
        <div>
            <div style={{
              display: 'inline-block', width: 700, paddingLeft: 55
            }}>
              <br></br>
              <Panel  shaded >
              <label style={{fontWeight: 'bold', fontSize:24, fontFamily: 'Times New Roman'}}> Model <GiInfo title = "create,edit, or delete"/> </label>
              <Link to='/createModel'>
                    <button style={{ float: 'right', fontWeight: 'bold', fontSize:18}} title="New Model" > + </button>
                </Link>
              <br></br><br></br>
                No models created yet. Please click "New Model"<br></br><br></br>
			  <tbody>
		        {LocalSotrageContent}
		      </tbody>		

			  </Panel>
              <br></br>
              <Panel  shaded >
              <label style={{fontWeight: 'bold', fontSize:24, fontFamily: 'Times New Roman'}}> Download Data</label>
              <br></br><br></br>
          
        
                <Button onClick={saveJSON} style = {{fontSize:12, fontFamily: 'Rockwell', width:100}}>Download Parameters in JSON</Button>
           
                <Button onClick={saveImage} style = {{fontSize:12, fontFamily: 'Rockwell', width:100}}>Download Image of Graph</Button>
                
                <Button onClick={saveCSV} style = {{fontSize:12, fontFamily: 'Rockwell', width:100}}>Download Graph Data in CSV</Button>
             

  				    <br></br><br></br><br></br>
              
            </Panel>
            </div>

            <div className = "graph">
                <Panel shaded>
                    <label style={{fontWeight: 'bold', fontSize:24, fontFamily: 'Times New Roman'}}> Plot <GiInfo title = "Plots for all created model"/></label>
                    <br></br><br></br>
                    This is the panel for graph
                </Panel>
            </div>

        </div>

    );
  }
}
export default The21cmSense;
