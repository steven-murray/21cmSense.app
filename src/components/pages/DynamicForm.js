import '../../App.css';
import React from 'react';
import { FormContext } from '../../FormContext';

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
      ant:[],
	  DataisLoaded: false
    }
  }

  componentDidMount(){

             fetch("http://localhost:8080/api-1.0/schema/calculation")
            .then((res) => res.json())
            .then((json) => {
                this.setState({
                    calc: json
                });
            })

            fetch("http://localhost:8080/api-1.0/schema/antenna/get/hera")
                      .then((res) => res.json())
                      .then((json) => {
                          this.setState({
                              ant: json,
							  DataisLoaded: true
                          });
                      })
    }

 render() {
    const { calc,ant,DataisLoaded } = this.state;              
 		if (!DataisLoaded) return <div>
			<h1> Pleses wait some time.... </h1> </div> ;

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
                   					<input type = {ant.data.antenna.hex_num.type} min = {ant.data.antenna.hex_num.minimum} placeholder = {ant.data.antenna.hex_num.help}/>
								</div> 								 
							</div>
							<br></br>
							<div class="row">
                    			<div>   
									<label> Separation </label>            
                   					<input type = {ant.data.antenna.separation.type} min = {ant.data.antenna.separation.minimum} placeholder = {ant.data.antenna.separation.help}/>
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