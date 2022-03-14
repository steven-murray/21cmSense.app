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

class CreateModel extends React.Component {
	
	  static propTypes = {
	    cookies: instanceOf(Cookies).isRequired
	  };
	
	 
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
			DishSizeUnits: '',
			FrequencyUnits: '',
			LatitudeUnits: '',
			Antenna: [],
			Beam: [],
			Location: [],			
			DataisLoaded: false,
			user: this.props.cookies.get("user") || ""
	
	    }
	  }
	
	 componentDidMount(){	
			if (document.cookie.indexOf('user') === -1 ) {
				// this.setState({notice: "I got it"});
				this.generateUserID();
			}		
				
			this.getAntennaData();	
			this.getBeamData();
			this.getLocationData();
	}

	generateUserID(){
		const { cookies } = this.props;
		const requestOptions = {
	        method: 'POST'
	    };
	    fetch('http://galileo.sese.asu.edu:8081/api-1.0/users', requestOptions)
	        .then(response => response.json())
	        .then(data => this.setState( cookies.set("user",data.uuid, { path: "/" }) ));
		
		
	}
	
	generateModel(uid){
		
		const ml = {
					  "modelname": this.state.modelName,
					  "data":{
							  "calculation": "1D-cut-of-2D-sensitivity",
							  "data":{
							    "antenna":{
							      "schema": "hera",
							      "hex_num": this.state.HexNumber,
							      "separation": this.state.Separation,
							      "dl": 12.02
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
	        method: 'POST',
				headers: { 'Content-Type': 'application/json' },
				body: JSON.stringify(ml)
			};
	
		    fetch('http://galileo.sese.asu.edu:8081/api-1.0/users/'+uid+'/models', requestmodel)
		}
	
	getAntennaData(){
            fetch("http://galileo.sese.asu.edu:8081/api-1.0/schema/antenna/get/hera")
                      .then((res) => res.json())
                      .then((json) => {
                          this.setState({
                              Antenna: json,
							  SeperationUnits: json.units.antenna.separation.default
                          });
                      })		
	}

	getBeamData(){
            fetch("http://galileo.sese.asu.edu:8081/api-1.0/schema/beam/get/GaussianBeam")
                      .then((ress) => ress.json())
                      .then((jsons) => {
                          this.setState({
                              Beam: jsons,
							  FrequencyUnits : jsons.units.beam.frequency.default,
							  DishSizeUnits : jsons.units.beam.dish_size.default
									
                          });
                      })		
	}
	
	getLocationData(){
            fetch("http://galileo.sese.asu.edu:8081/api-1.0/schema/location/get/latitude")
                      .then((resss) => resss.json())
                      .then((jsonss) => {
                          this.setState({
                              Location: jsonss,
							  LatitudeUnits : jsonss.units.location.latitude.default,
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
		this.generateModel(this.state.user);
	  };
	
	handleInputChange = (event) => {
	    const { name, value } = event.target;
			this.setState(() => ({
			    
			      [name]: value
			    }));
		};
	
render() {
		const { user } = this.state;
		const { Antenna,  Beam,Location, DataisLoaded} = this.state;      
		
		if (!DataisLoaded) return <div>
			<h1> Please wait some time.... </h1> </div> ;
	
	  return (
	
		 <div style={{display: 'block', width: 900, paddingLeft: 30 }}>
			<br></br><p>{user} </p> <br></br>
			<form onSubmit={this.handleOnSubmit} >
      		<Panel header = 'ANTENNA' shaded style={{color: 'rgb(77, 77, 58)', fontSize:21, fontFamily: 'Rockwell', paddingLeft: 20}}>		
				<label> Hex Number </label>            
                <input name = "HexNumber" type = {Antenna.data.antenna.hex_num.type} min = {Antenna.data.antenna.hex_num.minimum}  onChange={this.handleInputChange}   required/>
				<br></br><br></br>
				<label> Separation </label>           
                <input name = "Separation" type = {Antenna.data.antenna.separation.type} min = {Antenna.data.antenna.separation.minimum}  onChange={this.handleInputChange}   required/>
				<select name = "SeperationUnits" value={Antenna.units.antenna.separation.default} onChange={this.handleInputChange} >
			      {Antenna.units.antenna.separation.enum.map(o => <option value={o.value}>{o}</option>)}
			    </select>		
				<br></br><br></br>
			</Panel>
			<Panel header = 'BEAM' shaded  style={{color: 'rgb(77, 77, 58)', fontSize:21, fontFamily: 'Rockwell', paddingLeft: 20}}>
				<label> Dish Size </label>           
                <input name = "DishSize" type = {Beam.data.beam.dish_size.type} min={Beam.data.beam.dish_size.minimum}   onChange={this.handleInputChange}  required/>
				<select name = "DishSizeUnits" value={Beam.units.beam.dish_size.default} onChange={this.handleInputChange} >
			      {Beam.units.beam.dish_size.enum.map(o => <option value={o.value}>{o}</option>)}
			    </select>		
				<br></br><br></br>
				<label> Frequency </label>           
                <input name = "Frequency" type = {Beam.data.beam.frequency.type} min={Beam.data.beam.frequency.minimum}  onChange={this.handleInputChange} required/>
				<select name = "FrequencyUnits" value={Beam.units.beam.frequency.default} onChange={this.handleInputChange} >
			      {Beam.units.beam.frequency.enum.map(o => <option value={o.value}>{o}</option>)}
			    </select>
				<br></br><br></br>
			</Panel>
			<Panel header = 'LOCATION' shaded style={{color: 'rgb(77, 77, 58)', fontSize:21, fontFamily: 'Rockwell', paddingLeft: 20}}>
				<label> Latitude </label> 
				<input name = "Latitude"  type = {Location.data.location.latitude.type} min={Location.data.location.latitude.__minimum} max = {Location.data.location.latitude.__maximum}  onChange={this.handleInputChange}   required/>
				<select name = "LatitudeUnits" value={Location.units.location.latitude.default} onChange={this.handleInputChange} >
			      {Location.units.location.latitude.enum.map(o => <option value={o.value}>{o}</option>)}
			    </select>				
				<br></br><br></br>
			</Panel>
			<br></br><br></br>
			<label style = {{color: 'rgb(128, 0, 0)',  fontSize:18, fontFamily: 'Rockwell', width:180}}> Model Name </label>
			<input  name = "modelName" type = {"text"}  onChange={this.handleInputChange}  required />
			<Button onClick={ () => this.props.history.goBack() } style = {{fontSize:24, fontFamily: 'Rockwell', width:100}}> Cancel </Button>
			<Button  style = {{fontSize:24, fontFamily: 'Rockwell', width:100}} type="submit"
				disabled={localStorage.getItem(this.state.modelName)}> Save </Button>
			
			</form>
		</div>
  );
  }
}
	
export default withCookies(CreateModel);	