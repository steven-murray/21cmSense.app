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
                  <br></br><br></br><br></br>
                  <br></br><br></br>
                  <button><h5> PLOT </h5> </button>         
                  
            </form>
          </div>
          <div>
              <form >
                  <br></br>
                  <div class="row">
                    <div>
                      <DropDown options={calc}/>
                    </div>
                    <div>
                      <h6>CALCULATE</h6>
                    </div>
                  </div>
                  <br></br>
                  <br></br>
                  <div class="row">
                    <div>
                      <p><h6>Antenna Information</h6></p>
                    </div>
                    
                  </div>
                  <div class="row">
                    <div>   
						<label> Hex Number </label>            
                   		<input type = {hexObj.type} min = {hexObj.minimum} placeholder = {hexObj.help} />					
					</div>                    
                  </div>
                 <div class="row">
                   <div></div>
                   <div>
                   {}
                   </div> 
                   <div></div>
                                       
                  </div>
                  <div class="row">
                    <div>
                      <label> <h6>Beam Information</h6></label>
                    </div>
                    <div>
                      <DropDown options={groups}/>
                    </div>
                    
                  </div>
                  
                   <div class="row">
                    <div>
                      <label> <h6>Location Information</h6></label>
                    </div>
                    <div>
                      <DropDown options={groups}/>
                    </div>
                    
                  </div>
                  
              </form>
          </div>
        </div>        
       
      </div>
    </FormContext.Provider>

    );
  }
}
export default DynamicForm;