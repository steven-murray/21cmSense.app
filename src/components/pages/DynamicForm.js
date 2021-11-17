import '../../App.css';
import React,{ useState, useEffect, useMemo } from 'react';
import { FormContext } from '../../FormContext';
import ReactDOM from 'react-dom';

const DropDown = ({ selectedValue, disabled, options, onChange }) => {
  return (
    <select onChange={onChange} disabled={disabled}>
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
      groups: []
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
    this.setState({selectedGroup : e.target.value });
  }

  render() {
    const { schemas, groups} = this.state;
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
        />
        </form>
        
       </div>
    </FormContext.Provider>
    );
  }
}
export default DynamicForm;