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
      antenna:[{
                                        "__comment__": "this is an extension of the JSON schema document and includes 'default' specifier",
                                        "schema": "hera",
                                        "description": "Hera-class antenna array",
                                        "group": "antenna",
                                        "jsonSchema": {
                                            "required": [
                                                    "hex_num",
                                                    "separation",
                                                    "dl"
                                                ],
                                            "properties": {
                                                "hex_num": {
                                                    "type": "integer",
                                                    "minimum": 3,
                                                    "help": "Number of antennas per side of hexagonal array"
                                                },
                                                "separation": {
                                                    "type": "number",
                                                    "minimum": 0,
                                                    "help": "The distance between antennas along a side"
                                                },
                                                "dl": {
                                                    "type": "number",
                                                    "minimum": 0,
                                                    "help": "The distance between rows of antennas"
                                                },
                                                "separation_Unit": {
                                                      "type": "string",
                                                      "default": "m",
                                                      "enum": [
                                                          "m",
                                                          "s"
                                                      ]
                                                  },
                                                  "dl_Unit": {
                                                      "type": "string",
                                                      "default": "m",
                                                      "enum": [
                                                          "m",
                                                          "s"
                                                      ]
                                                  }
                                                  
                                              }
                                          }
                                     }],
      beam:[],
      location:[],
      schemas: [],
      groups: [],
      schema:[]
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

            fetch("http://localhost:8080/api-1.0/schema/antenna")
                      .then((res) => res.json())
                      .then((json) => {
                          this.setState({
                              groups: json
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
    const { calc,antenna,schemas, groups, schema } = this.state;                                        

    return (
    <FormContext.Provider>
        
      <div className="container">
         <div class="row">
          <div>
            <form >
                  <br></br>
                  <h6>MODELS</h6>  
                  <br></br><br></br><br></br>
                  <br></br><br></br><br></br>
                  <br></br><br></br><br></br>
                  <br></br><br></br><br></br>
                  <br></br><br></br><br></br>
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
                      <label> <h6>CALCULATE</h6></label>
                    </div>
                  </div>
                  <br></br>
                  <br></br>
                  <div class="row">
                    <div>
                      <label> <h6>Antenna Information</h6></label>
                    </div>
                    <div>
                      <DropDown options={groups}/>
                    </div>
                    
                  </div>
                  <div class="row">
                    <Form schema={antenna[0].jsonSchema}/>
                                       
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
                    <Form schema={antenna[0].jsonSchema}/>
                                       
                  </div>
                   <div class="row">
                    <div>
                      <label> <h6>Location Information</h6></label>
                    </div>
                    <div>
                      <DropDown options={groups}/>
                    </div>
                    
                  </div>
                  <div class="row">
                    <Form schema={antenna[0].jsonSchema}/>
                                       
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