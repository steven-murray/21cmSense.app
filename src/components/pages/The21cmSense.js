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
			_models:[],
			calc:[],
			pmodel : [],
			
			HexNumber: '',
			Separation: '',	
			DishSize: '',
			Frequency: '',
			Latitude: '',
			SeperationUnits: '',
			DishSizeUnits: '',
			FrequencyUnits: '',
			LatitudeUnits: ''
	    }
	  }
	  
	  componentDidMount(){
		const modelid = 'b5749a3c-d395-427c-8478-0af262cac35a';	
		const {user}=this.state;
		if(user !== ""){
		this.getmodels(user);
		this.getmodel(user,modelid);
		}
		
		

		 fetch("http://galileo.sese.asu.edu:8081/api-1.0/schema/calculation")
            .then((res) => res.json())
            .then((json) => {
                this.setState({
                    calc: json
                });
            })
	  }

	  getmodels(uid){
            fetch('http://galileo.sese.asu.edu:8081/api-1.0/users/'+uid+'/models')
                      .then((res) => res.json())
                      .then((json) => {
                          this.setState({
                              _models: json.models
                          });  
                      })		
	  };

	getmodel(uid,mid){
	
            fetch('http://galileo.sese.asu.edu:8081/api-1.0/users/fd1039f8-76b5-495f-9d9b-bbb20520d7b9/models/1fd53fc3-7fec-4f37-ba24-8d1ec96103a1')
                      .then((res) => res.json())
                      .then((json) => {
                          this.setState({
                            model: json,
							model_id: mid,
							modelName: json.modelname,
							HexNumber: json.data.data.antenna.hex_num,
							Separation: json.data.data.antenna.separation,	
							DishSize: json.data.data.beam.dish_size,
							Frequency: json.data.data.beam.frequency,
							Latitude: json.data.data.location.latitude,	
							SeperationUnits: json.data.units.antenna.separation,
							DishSizeUnits: json.data.units.beam.dish_size,
							FrequencyUnits: json.data.units.beam.frequency,
							LatitudeUnits: json.data.units.location.latitude
                          }); 
                      })		
	}
	
	generateCalcModel(mid){
		
		const ml = 
					  {
						  "calculation": "1D-cut-of-2D-sensitivity",
						  "data":{
						    "antenna":{
						      "schema": "hera",
						      "hex_num": 7,
						      "separation": 14,
						      "dl": 12.02
						    },
						    "beam":{
						      "schema":"GaussianBeam",
						      "frequency": 100,
						      "dish_size": 14
						    },
						    "location":{
						      "schema": "latitude",
						      "latitude": 1.382
						    }
						  },
						  "units":{
						    "antenna":{
						      "hex_num": "m",
						      "separation": "m",
						      "dl": "m"
						    },
						    "beam":{
						      "frequency": "MHz",
						      "dish_size": "m"
						    },
						    "location":{
						      "latitude": "deg"
						    }
						  }
						}
				
		const requestmodel = {
	        method: 'POST',
				headers: { 'Content-Type': 'application/json' },
				body: JSON.stringify(ml)
			};
	
		    fetch('http://galileo.sese.asu.edu:8081/api-1.0/users/fd1039f8-76b5-495f-9d9b-bbb20520d7b9/models' + mid, requestmodel)
					.then((res) => res.json())
                      .then((json) => {
                          this.setState({
                              pmodel: json
                          }); console.log(json) 
                      })	
		console.log(this.state.pmodel);
	}
	

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
			  <div   style={{color: 'rgb(77, 77, 58)', fontSize:21, fontFamily: 'Rockwell', paddingLeft: 20}}>
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
			<form >
                <Panel shaded>
                    <label style={{fontWeight: 'bold', fontSize:24, fontFamily: 'Times New Roman'}}> Plot <GiInfo title = "Plots for all created model"/></label>
                    <br></br><br></br>
					<label style = {{fontSize:21, fontFamily: 'Rockwell', width:100}}> Calculation </label>           
	                <select name = "Calculation"  >
				      {this.state.calc.map(o => <option value={o.value}>{o}</option>)}
				    </select>
					<label style = {{fontSize:21, fontFamily: 'Rockwell', width:100}}> Models </label>           
	                <select name = "models">						
						 {this.state._models.map(dataIn => <option value={dataIn.modelname}>{dataIn.modelname}</option>)}						     
					</select>
 					<br></br><br></br>
					<Button  style={{color: 'rgb(77, 77, 58)', fontSize:21, fontFamily: 'Rockwell', paddingLeft: 20}} onClick = {this.generateCalcModel.bind(this,'b5749a3c-d395-427c-8478-0af262cac35a')}> Save </Button>		
                </Panel>
			
                    
			</form>
            </div>

        </div>

    );
  }
}
export default withCookies(The21cmSense);
