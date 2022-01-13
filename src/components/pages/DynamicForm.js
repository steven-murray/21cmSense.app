import '../../App.css';
import React,{ useState, useEffect, useMemo } from 'react';
import { FormContext } from '../../FormContext';

import ReactDOM from 'react-dom';
import Form from "react-jsonschema-form";
import  { Component } from "react";

const DropDown = ({ selectedValue, options, onChange }) => {
  return (
    <select onChange={onChange} >
      {
        options.map(o => <option value={o} selected={o == selectedValue}>{o}</option>)
        
      }
    </select>
  );
}


class DynamicForm extends React.Component {


  constructor(props) {
    super(props);
    this.state = {
      calc:[],
      antenna:[],
      beam:[],
      location:[],
      schemas: [],
      groups: [],
      schema:[],
      requires:[]
    }
    

    this.onSchemasChange = this.onSchemasChange.bind(this);
    this.onGroupsChange = this.onGroupsChange.bind(this);
    
  }

  componentDidMount(){

             fetch("http://localhost:8080/api-1.0/schema/calculation")
            .then((res) => res.json())
            .then((json) => {
                this.setState({
                    calc: json
                });
            })

            fetch("http://localhost:8080/api-1.0/schema")
            .then((res) => res.json())
            .then((json) => {
                this.setState({
                    schemas: json
                });
            })

            fetch("http://localhost:8080/api-1.0/schema/antenna/get/hera")
                      .then((res) => res.json())
                      .then((json) => {
                          this.setState({
                              antenna: json
                          });
                      })
    }

         
  onSchemasChange(e) {
    var group = e.target.value;
    
          fetch("http://localhost:8080/api-1.0/schema/" + group )
            .then((res) => res.json())
            .then((json) => {
                this.setState({
                    groups: json
                });
            })
  }

  onGroupsChange(e) {
    var forms = e.target.value;
          fetch("http://localhost:8080/api-1.0/schema/antenna/get/"+ forms)
            .then((res) => res.json())
            .then((json) => {
                this.setState({
                    schema: json
                });
            })

  }

 
  render() {
    const { calc,antenna,schemas, groups, schema,requires } = this.state;              
    const myObj = antenna;
	const hexObj = {
        "type": "integer",
        "minimum": 3,
        "help": "Number of antennas per side of hexagonal array"
      }                    
      let text ="" ;
      let la = "DL";

      for (const x in myObj) {
         if(x == "data"){
              for(const y in myObj[x]){
                if(y == "antenna"){
                  for(const z in myObj[x][y]){
	
                    if (z == "hex_num"){
					//	hexObj = JSON.parse(myObj[x][y][z]);
					}
                    
                  }
               }
              }
        }

      }

    return (
    <FormContext.Provider>
        
      <div className="container">
         <div class="row">
          <div>
            <form >
                  <br></br>
                  <h6>MODELS</h6>  
						Example 1 <br></br>
						Example 2  <br></br>
						Example 3  <br></br>
						Example 4  <br></br>
						Example 5  <br></br>
						Example 6  <br></br>
						Example 7  <br></br>
						Example 8  <br></br>
						<br></br>
                 <p> <button><h5> PLOT </h5> </button> </p>                  
            </form>
          </div>
          <div>
            	<br></br>
                <div class="row">
                    <div>  <DropDown options={calc}/> 	
						   <br></br><br></br>
 							<div class="row">
                    			<div> <p><h6>Antenna Information</h6></p> </div>                    
                			</div>
                			<div class="row">
                    			<div>   
									<label> Hex Number </label>            
                   					<input type = {hexObj.type} min = {hexObj.minimum} placeholder = {hexObj.help} />					
								</div>                    
                			</div>

					</div>
                    <div> <h6>CALCULATE</h6>   </div>
                </div>			
          </div>
        </div>
      </div>        
   </FormContext.Provider>
  );
  }
}
export default DynamicForm;