import '../../App.css';
import formJSON from '../../schema/formElement.json';
import React,{ useState, useEffect } from 'react';
import Element from '../Element';
import { FormContext } from '../../FormContext';




function DynamicForms() {

  const myUrl = "http://localhost:8080/api-1.0/schema"; 
  
  window.onload = () => {
        var select = document.getElementById("selectSchema");

        var options = ["antenna", "beam", "calculation", "location"];
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
        <form>
              <select id="selectSchema">
                <option>Choose a Schema</option>
              </select> 
        </form>

      </div>
    </FormContext.Provider>
    
  );
}



export default DynamicForms;
