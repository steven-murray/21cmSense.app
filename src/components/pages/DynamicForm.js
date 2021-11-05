import '../../App.css';
import formJSON from '../../schema/formElement.json';
import React,{ useState, useEffect } from 'react';
import Element from '../Element';
import { FormContext } from '../../FormContext';




function DynamicForms() {

  const myUrl = "http://localhost:8080/api-1.0/schema"; 
  const schemas = ["antenna", "beam", "calculation", "location"]

  for (var i = 0; i<= schemas.length; i++) {
  
    document.write(schemas[i]);
  
    document.write("<br />");
  }


  return (
    <FormContext.Provider>
      <div className="App container">
        <h3>"21cmsense Dynamic Form"</h3>
        <form>
                     
        </form>

      </div>
    </FormContext.Provider>
    
  );
}



export default DynamicForms;
