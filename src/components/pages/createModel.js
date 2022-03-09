import '../../App.css';
import React from 'react';
import { Panel } from 'rsuite';
import styled from "styled-components";
import { withRouter } from 'react-router-dom';


const DropDown = ({ selectedValue, options, onChange }) => {
  return (
    <select onChange={onChange} >
      {
        options.map(o => <option value={o} selected={o === selectedValue}>{o}</option>)
        
      }
    </select>
  );
}

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
			
		  	Antenna: [],
			Beam: [],
			DataisLoaded: false
	    }

	  }

	 componentDidMount(){

			this.getAntennaData();
			
			this.getBeamData();
    }

	getAntennaData(){
            fetch("http://galileo.sese.asu.edu:8081/api-1.0/schema/antenna/get/hera")
                      .then((res) => res.json())
                      .then((json) => {
                          this.setState({
                              Antenna: json
                          });
                      })		
	}

	getBeamData(){
            fetch("http://galileo.sese.asu.edu:8081/api-1.0/schema/beam/get/GaussianBeam")
                      .then((ress) => ress.json())
                      .then((jsons) => {
                          this.setState({
                              Beam: jsons,
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
	  };
	
	handleInputChange = (event) => {
	    const { name, value } = event.target;
			this.setState((prevState) => ({
			      ...prevState,
			      [name]: value
			    }));
		};

render() {
		
		const { Antenna} = this.state;      
		const { Beam, DataisLoaded} = this.state;           
 		if (!DataisLoaded) return <div>
			<h1> Please wait some time.... </h1> </div> ;
			
		const option = {
						 "separation": {
							        "type": "string",
							        "default": "m",
							        "enum": [
							          "m",
							          "s"
							        ]
							      },
						"frequency": {
							"type": "string",
							        "default": "MHz",
							        "enum": [
							          "MHz"
							        ]
						}
						}
						
		
		
		
     return (
		 <div style={{display: 'block', width: 900, paddingLeft: 30 }}>
			<br></br>
			
			<form onSubmit={this.handleOnSubmit} >
      		<Panel header = 'ANTENNA' shaded style={{color: 'rgb(77, 77, 58)', fontSize:21, fontFamily: 'Rockwell', paddingLeft: 20}}>
				<label> Hex Number </label>            
                <input name = "HexNumber" type = {Antenna.data.antenna.hex_num.type} min = {Antenna.data.antenna.hex_num.minimum}  onChange={this.handleInputChange}   required/>
				<br></br><br></br>
				<label> Separation </label>           
                <input name = "Separation" type = {Antenna.data.antenna.separation.type} min = {Antenna.data.antenna.separation.minimum}  onChange={this.handleInputChange}   required/>
				<DropDown name = "SeperationUnits" type = {Antenna.units.antenna.separation.type} default = {Antenna.units.antenna.separation.default} options={Antenna.units.antenna.separation.enum}  onChange={this.handleInputChange}  />      
  				<br></br><br></br>
			</Panel>
			<Panel header = 'BEAM' shaded  style={{color: 'rgb(77, 77, 58)', fontSize:21, fontFamily: 'Rockwell', paddingLeft: 20}}>
				<label> Dish Size </label>           
                <input name = "DishSize" type = {Beam.data.beam.dish_size.type} min={Beam.data.beam.dish_size.minimum}   onChange={this.handleInputChange}  required/>
				<DropDown name = "DishSizeUnits"  type = {Beam.units.beam.dish_size.type}  options={Beam.units.beam.dish_size.enum}  />      
  				<br></br><br></br>
				<label> Frequency </label>           
                <input name = "Frequency" type = {Beam.data.beam.frequency.type} min={Beam.data.beam.frequency.minimum}  onChange={this.handleInputChange} required/>
				<DropDown name = "FrequencyUnits"   type = {Beam.units.beam.frequency.type}  options={Beam.units.beam.frequency.enum}/>      
  				<br></br><br></br>
			</Panel>
			<Panel header = 'LOCATION' shaded style={{color: 'rgb(77, 77, 58)', fontSize:21, fontFamily: 'Rockwell', paddingLeft: 20}}>
				<label> Latitude </label> 
				<input name = "Latitude"  type = {"number"} min={-180} max = {180}  onChange={this.handleInputChange}   required/>
				<DropDown name = "LatitudeUnits" options={option.separation.enum}/>      
  				<br></br><br></br>
			</Panel>
			<br></br><br></br>
			<label style = {{color: 'rgb(128, 0, 0)',  fontSize:18, fontFamily: 'Rockwell', width:180}}> Model Name </label>
			<input  name = "modelName" type = {"text"}  value={this.state.modelName} onChange={this.handleInputChange} required />
			<Button onClick={ () => this.props.history.goBack() } style = {{fontSize:24, fontFamily: 'Rockwell', width:100}}> Cancel </Button>
			<Button  style = {{fontSize:24, fontFamily: 'Rockwell', width:100}} type="submit"
				disabled={localStorage.getItem(this.state.modelName)} > Save </Button>
			
			</form>
		</div>
  );
  }
}
	
export default withRouter(CreateModel);	