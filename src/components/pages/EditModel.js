import '../../App.css';
import React from 'react';
import { Panel } from 'rsuite';
import styled from "styled-components";
import { withCookies, Cookies } from "react-cookie";
import { instanceOf } from "prop-types";

const theme = {
  blue: {
    default: "#9facde",
    hover: "#657aca"
  },
  green: {
    default: "#6ca59b",
    hover: "#6c9ca5"
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
  theme: "green"

};

class EditModel extends React.Component {
	
	  static propTypes = {
	    cookies: instanceOf(Cookies).isRequired
	  };
	
	 
	 constructor(props) {
	    super(props);
	    this.state = {
			model_id:'',
			modelName: '',
			models: [],
			model: [],
			
		  	
			HexNumber: '',
			HexType:'',
			HexMin:'',
			
		  	Separation: '',	
			SepType:'',
			SepMin:'',
			SepEnum: [],
			
		  	DishSize: '',
			DSType: '',
			DSMin: '',
			DSEnum: [],
			
		  	Frequency: '',
			FreType: '',
			FreMin: '',
			FreEnum: [],
			
		  	Latitude: '',
			LaType: '',
			LaMin: '',
			LaMax: '',
			LaEnum: [],
	
		  	SeperationUnits: '',
			DishSizeUnits: '',
			FrequencyUnits: '',
			LatitudeUnits: '',
			
			DataisLoaded: false,
			user: this.props.cookies.get("user") || ""
	
	    }
	  }
	
	 componentDidMount(){	
			const{modelid}=(this.props.location && this.props.location.state) || {} 
			
			const {user}=this.state;
			this.getmodel(user,modelid);			
			this.getmodels(user);
			
			
			this.getAntennaData();	
			this.getBeamData();
			this.getLocationData();
	}
	

	getmodels(uid){
            fetch('http://galileo.sese.asu.edu:8081/api-1.0/users/'+uid+'/models')
                      .then((res) => res.json())
                      .then((json) => {
                          this.setState({
                              models: json.models
                          });   
                      })		
	}
	
	getmodel(uid,mid){
	
            fetch('http://galileo.sese.asu.edu:8081/api-1.0/users/'+uid+'/models/' + mid)
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

	
	updateModel(uid,mid){
		
		const ml = {
					  "modelname": this.state.modelName,
					  "data":{
							  "calculation": "1D-cut-of-2D-sensitivity",
							  "data":{
							    "antenna":{
							      "schema": "hera",
							      "hex_num": this.state.HexNumber,
							      "separation": this.state.Separation
							    },
							    "beam":{
							      "schema":"GaussianBeam",
							      "frequency": this.state.Frequency,
							      "dish_size": this.state.DishSize
							    },
							    "location":{
							      "schema": "latitude",
							      "latitude": this.state.Latitude
							    }
							  },
							  "units":{
							    "antenna":{
							      "hex_num": "m",
							      "separation": this.state.SeperationUnits,
							      "dl": "m"
							    },
							    "beam":{
							      "frequency": this.state.FrequencyUnits,
							      "dish_size": this.state.DishSizeUnits
							    },
							    "location":{
							      "latitude": this.state.LatitudeUnits
							    }
							  }
							}
					}
		
		const requestmodel = {
	        method: 'PUT',
				headers: { 'Content-Type': 'application/json' },
				body: JSON.stringify(ml)
			};
	
		    fetch('http://galileo.sese.asu.edu:8081/api-1.0/users/'+uid+'/models/' + mid, requestmodel)
		}
	
	getAntennaData(){
            fetch("http://galileo.sese.asu.edu:8081/api-1.0/schema/antenna/get/hera")
                      .then((res) => res.json())
                      .then((json) => {
                          this.setState({
                              SeperationUnits: json.units.antenna.separation.default,
							  HexType: json.data.antenna.hex_num.type,
							  HexMin: json.data.antenna.hex_num.minimum,								
							  SepType: json.data.antenna.separation.type,
							  SepMin: json.data.antenna.separation.minimum,
							  SepEnum: json.units.antenna.separation.enum
								
							
                          });
                      })		
	}

	getBeamData(){
            fetch("http://galileo.sese.asu.edu:8081/api-1.0/schema/beam/get/GaussianBeam")
                      .then((ress) => ress.json())
                      .then((jsons) => {
                          this.setState({
                              FrequencyUnits : jsons.units.beam.frequency.default,
							  DishSizeUnits : jsons.units.beam.dish_size.default,
							  DSType: jsons.data.beam.dish_size.type,
							  DSMin: jsons.data.beam.dish_size.minimum,
							  DSEnum: jsons.units.beam.dish_size.enum,
							  FreType: jsons.data.beam.frequency.type,
							  FreMin: jsons.data.beam.frequency.minimum,
							  FreEnum: jsons.units.beam.frequency.enum
									
                          });
                      })		
	}
	
	getLocationData(){
            fetch("http://galileo.sese.asu.edu:8081/api-1.0/schema/location/get/latitude")
                      .then((resss) => resss.json())
                      .then((jsonss) => {
                          this.setState({
                              LatitudeUnits : jsonss.units.location.latitude.default,					
							  LaType: jsonss.data.location.latitude.type,
							  LaMin: jsonss.data.location.latitude.__minimum,
							  LaMax: jsonss.data.location.latitude.__maximum,
							  LaEnum: jsonss.units.location.latitude.enum,
							  DataisLoaded: true		
                          });
                      })		
	}
		
	handleOnSubmit = (event) => {
	    event.preventDefault();	
			    this.props.history.push({
	      pathname: '/The21cmSense',
	      state : this.state
	    });	
		this.updateModel(this.state.user, this.state.model_id);
	  };
	
	handleInputChange = (event) => {
	    const { name, value } = event.target;
			this.setState(() => ({
			    
			      [name]: value
			    }));
		};
	
render() {
		const {DataisLoaded} = this.state;      
		
		if (!DataisLoaded) return <div>
			<h1> Please wait some time.... </h1> </div> ;
	
	  return (
	
		 <div style={{display: 'block', width: 900, paddingLeft: 30 }}>
			<br></br><br></br>
			<form onSubmit={this.handleOnSubmit} >
      		<Panel header = 'ANTENNA' shaded style={{color: 'rgb(77, 77, 58)', fontSize:21, fontFamily: 'Rockwell', paddingLeft: 20}}>		
				<label> Hex Number </label>            
                <input name = "HexNumber" type = {this.state.HexType} min = {this.state.HexMin} defaultValue={this.state.HexNumber} onChange={this.handleInputChange}   required/>
				<br></br><br></br>
				<label> Separation </label>           
                <input name = "Separation" type = {this.state.SepType} min = {this.state.SepMin} defaultValue={this.state.Separation} onChange={this.handleInputChange}   required/>
				<select name = "SeperationUnits" value={this.state.SeperationUnits} onChange={this.handleInputChange} >
			      {this.state.SepEnum.map(o => <option value={o.value}>{o}</option>)}
			    </select>		
				<br></br><br></br>
			</Panel>
			<Panel header = 'BEAM' shaded  style={{color: 'rgb(77, 77, 58)', fontSize:21, fontFamily: 'Rockwell', paddingLeft: 20}}>
				<label> Dish Size </label>           
                <input name = "DishSize" type = {this.state.DSType} min={this.state.DSMin} defaultValue={this.state.DishSize}  onChange={this.handleInputChange}  required/>
				<select name = "DishSizeUnits" value={this.state.DishSizeUnits} onChange={this.handleInputChange} >
			      {this.state.DSEnum.map(o => <option value={o.value}>{o}</option>)}
			    </select>		
				<br></br><br></br>
				<label> Frequency </label>           
                <input name = "Frequency" type = {this.state.FreType} min={this.state.FreMin} defaultValue={this.state.Frequency} onChange={this.handleInputChange} required/>
				<select name = "FrequencyUnits" value={this.state.FrequencyUnits} onChange={this.handleInputChange} >
			      {this.state.FreEnum.map(o => <option value={o.value}>{o}</option>)}
			    </select>
				<br></br><br></br>
			</Panel>
			<Panel header = 'LOCATION' shaded style={{color: 'rgb(77, 77, 58)', fontSize:21, fontFamily: 'Rockwell', paddingLeft: 20}}>
				<label> Latitude </label> 
				<input name = "Latitude"  type = {this.state.LaType} min={this.state.LaMin} max = {this.state.LaMax} defaultValue={this.state.Latitude} onChange={this.handleInputChange}   required/>
				<select name = "LatitudeUnits" value={this.state.LatitudeUnits} onChange={this.handleInputChange} >
			      {this.state.LaEnum.map(o => <option value={o.value}>{o}</option>)}
			    </select>				
				<br></br><br></br>
			</Panel>
			<br></br><br></br>
			<label style = {{color: 'rgb(128, 0, 0)',  fontSize:18, fontFamily: 'Rockwell', width:180}}> Model Name </label>
			<input  name = "modelName" type = {"text"}  defaultValue = {this.state.modelName} onChange={this.handleInputChange} style = {{color: 'rgb(77, 77, 58)',  fontSize:18, fontFamily: 'Rockwell', width:180}} required />
			<Button onClick={ () => this.props.history.goBack() } style = {{fontSize:24, fontFamily: 'Rockwell', width:100}}> Cancel </Button>
			<Button  style = {{fontSize:24, fontFamily: 'Rockwell', width:100}} type="submit"
				disabled={this.state.models.some(model => model.modelname === this.state.modelName)}> Save </Button>
			
			</form>
		</div>
  );
  }
}
	
export default withCookies(EditModel);	