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
      schemas: [],
      groups: [],
      schema: [{
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
                                     }]
    }
    

    this.onSchemasChange = this.onSchemasChange.bind(this);
    this.onGroupsChange = this.onGroupsChange.bind(this);
    
  }

  componentDidMount(){

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
    const { schemas, groups, schema } = this.state;                                        

    return (
     <FormContext.Provider>
      <div className="App container">
        <h3>"21cmsense Dynamic Form"</h3>
          
        <form >
          <br></br>
          <h6> SCHEMA LIST</h6>              
        <DropDown
          options={schemas}
          onChange={this.onSchemasChange}
         
          

        />
        <br></br>
        <br></br>
        <h6> GROUP LIST</h6>
        <DropDown
          options={groups }
          onChange={this.onGroupsChange}
        />

        <br></br>
        <br></br>
        <h6> 21cmSense Form</h6>
        <h4> DATA </h4>
         <Form schema={schema[0].jsonSchema}/>
         
        </form>
       
       </div>
    </FormContext.Provider>
    );
  }
}
export default DynamicForm;