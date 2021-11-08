import '../../App.css';
import formJSON from '../../schema/formElement.json';
import React,{ useState, useEffect } from 'react';
import Element from '../Element';
import { FormContext } from '../../FormContext';



function DynamicForms() {

/*  var url = "http://192.168.1.11:8080/api-1.0/schema"; 
  let jsondata;    
  fetch(url).then(
        function(u){ return u.json();}
      ).then(
        function(json){
          jsondata = json;
        }
      )*/
  window.onload = () => {
        var select = document.getElementById("selectSchema");

        var options =  ["antenna", "beam", "calculation", "location"];
        for(var i = 0; i < options.length; i++) {
            var opt = options[i];
            var el = document.createElement("option");
            el.textContent = opt;
            el.value = opt;
            select.appendChild(el);
        }
  }



  return (
    <FormContext.Provider>
      <div className="App container">
        <h3>"21cmsense Dynamic Form"</h3>
          
        <form >
          <br></br>
          <h6> SCHEMA LIST</h6>                
          <select id="selectSchema">
               <option>Choose a Schema</option>
          </select> 

        </form>

      </div>
    </FormContext.Provider>
    
  );
}



export default DynamicForms;
