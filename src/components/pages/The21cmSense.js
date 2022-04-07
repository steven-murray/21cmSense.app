import React from 'react';
import '../../App.css';
import { Panel } from 'rsuite';
import '../rsuite-default.css';
import { GiInfo, GiPencil, GiEmptyWoodBucket } from "react-icons/gi";
import { Link } from 'react-router-dom';
import '../../TestGraphDownload.js';
import { saveAs } from "file-saver";
import styled from "styled-components";
import { withCookies, Cookies } from "react-cookie";
import { instanceOf } from "prop-types";


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
	
	
	 static propTypes = {
	    cookies: instanceOf(Cookies).isRequired
	  };
	
	constructor(props) {
	    super(props);
		
	    this.state = {
			selectOptions: [],
	     	user:this.props.cookies.get("user") || "",
			LatitudeUnits: '',
			_models:[]
	    }
	  }
	  
	  componentDidMount(){	
		const {user}=this.state;
		if(user !== ""){
		this.getmodels(user);
		}
		
	  }

	  getmodels(uid){
            fetch('http://galileo.sese.asu.edu:8081/api-1.0/users/'+uid+'/models')
                      .then((res) => res.json())
                      .then((json) => {
                          this.setState({
                              _models: json.models
                          });  console.log(json);
                      })		
	  };
	
	handleOnSubmit = (event) => {
		// event.preventDefault();	
			    this.props.history.push({
	      pathname: '/EditModel',
	      state : event
	    });	

	  };
	
	deletemodule(mid){
	    const req = {
	        method: 'DELETE'
			};
	
		    fetch('http://galileo.sese.asu.edu:8081/api-1.0/users/'+this.state.user+'/models/' + mid, req)
				.then(response => {window.location.reload()});
	}

  render() {
	
	  const {_models} = this.state	
	  const resume = _models.map(dataIn => {
      return (
        <div key={dataIn.modelid}>
          {dataIn.modelname}
          <button style={{ float: 'right',  fontSize:18}} title="Delete Model" onClick = {this.deletemodule.bind(this, dataIn.modelid)} > <GiEmptyWoodBucket title = "delete"/>  </button>       
          <button style={{ float: 'right',  fontSize:18}} title="Edit Model" onClick = {this.handleOnSubmit.bind(this, dataIn) } > <GiPencil title = "edit"/>  </button>   
		  
		  </div>
      );
    });
    return (
        <div>
            <div style={{
              display: 'inline-block', width: 700, paddingLeft: 35
            }}>
              <br></br> 
              <Panel  shaded >
              <label style={{fontWeight: 'bold', fontSize:24, fontFamily: 'Times New Roman'}}> Model <GiInfo title = "create,edit, or delete"/> </label>
              <Link to='/createModel'>
                    <button style={{ float: 'right', fontWeight: 'bold', fontSize:18}} title="New Model" > + </button>
                </Link>
              <br></br><br></br>
                No models created yet. Please click "New Model"<br></br><br></br>
			  <div   style={{ display: 'inline-block', color: 'rgb(77, 77, 58)', fontSize:21, fontFamily: 'Rockwell', paddingLeft: 20}}>
		      		 {resume}  
		      </div>	
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
export default withCookies(The21cmSense);
