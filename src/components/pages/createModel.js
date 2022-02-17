import '../../App.css';
import React from 'react';
import { Panel } from 'rsuite';
import styled from "styled-components";


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
     
    }
  }



render() {
		const option = {
						 "separation": {
							        "type": "string",
							        "default": "m",
							        "enum": [
							          "m",
							          "s"
							        ]
							      }
						}
		
     return (
		 <div style={{display: 'block', width: 900, paddingLeft: 30 }}>
			<br></br>
			<form >
      		<Panel header = 'ANTENNA' shaded style={{color: 'rgb(77, 77, 58)', fontSize:21, fontFamily: 'Rockwell', paddingLeft: 20}}>
				<label> Hex Number </label>            
                <input type = {"number"} min={3}   required/>
				<br></br><br></br>
				<label> Separation </label>           
                <input type = {"number"} min={0}   required/>
				<DropDown options={option.separation.enum}/>      
  				<br></br><br></br>
				<label> Distance </label>           
                <input type = {"number"} min={0}   required/>
				<DropDown options={option.separation.enum}/>      
  				<br></br><br></br>
			</Panel>
			<Panel header = 'BEAM' shaded  style={{color: 'rgb(77, 77, 58)', fontSize:21, fontFamily: 'Rockwell', paddingLeft: 20}}>
				<label> Dish Size </label>           
                <input type = {"number"} min={0}   required/>
				<DropDown options={option.separation.enum}/>      
  				<br></br><br></br>
			</Panel>
			<Panel header = 'LOCATION' shaded style={{color: 'rgb(77, 77, 58)', fontSize:21, fontFamily: 'Rockwell', paddingLeft: 20}}>
				<label> Latitude </label> 
				<input type = {"number"} min={-180} max = {180}   required/>
				<DropDown options={option.separation.enum}/>      
  				<br></br><br></br>
			</Panel>
			<br></br><br></br>
			<label style = {{color: 'rgb(128, 0, 0)',  fontSize:18, fontFamily: 'Rockwell', width:180}}> Model Name </label>
			<input type = {"text"}  required/>
			<Button onClick={ () => this.props.history.goBack() } style = {{fontSize:24, fontFamily: 'Rockwell', width:100}}> Cancel </Button>
			<Button  style = {{fontSize:24, fontFamily: 'Rockwell', width:100}}> Save </Button>
			
			</form>
		</div>
  );
  }
}
	
export default CreateModel;	