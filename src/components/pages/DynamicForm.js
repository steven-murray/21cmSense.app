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
    const { hexObj,calc,antenna,schemas, groups, schema,requires } = this.state;              
    const myObj = {"__comment__": "this is an extension of the JSON schema document and includes default specifier","schema": "hera","description": "Hera-class antenna array","group": "antenna","data":{"antenna":{"hex_num": {"type": "integer", "minimum": 3, "help": "Number of antennas per side of hexagonal array" },  "separation": { "type": "number", "minimum": 0, "help": "The distance between antennas along a side"}, "dl": { "type": "number", "minimum": 0,"help": "The distance between rows of antennas"}},"required": ["hex_num","separation","dl"]}};
         
                               
      let text  ;
      let la = "DL";
      for (const x in myObj) {
       // text += x +",";
        if(x == "data"){
              for(const y in myObj[x]){
                if(y == "antenna"){
                 // text += myObj[x][y]+",";
                  for(const z in myObj[x][y]){
                    text +=z +",";
                    
                  }
                 // text += "</select>";
               //   document.getElementById("text").innerHTML = text
                }
              }
        }
        //for(const y in myObj[x]){
      
     /*     if (y == "required"){
                 text =myObj[x][y];
            
            
          }*/
        /*  for(const z in myObj[x][y]){
            //text += z + ",";
            if(z == schemas[0]){
              text += "found it";
            }else{
              text+=z + ",";
            }
           // for(const t in myObj[x][y][z]){
           //       text += t + ",";
           // }
            
          }
      // text += myObj[x][y]+ "., ";*/
     //   }
      
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
                    <div>
                      {text.antenna}
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