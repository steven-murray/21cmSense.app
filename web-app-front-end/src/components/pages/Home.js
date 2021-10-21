import React, {Component} from 'react';
import DynamicForm from "./DynamicForm";
import '../../App.css';


class Home extends Component {
	state = {
	  data: [
	    {
		 antenna_hex_number: 1,
		 separation: 1,
		 separation_units: "Mhz",
		 dl: 0,
		 beam: "type",
		 frequency: 2,
		 frequency_units: "Mhz",
		 dish_size: 1,
		 dish_size_units: "m",
		 location: "180"
   
	    }
   
	  ],
	  current: {}
	
	};
   
   
	onSubmit = model => {
	  let data = [];
	  if (model.antenna_hex_number) {
	    data = this.state.data.filter(d => {
		 return d.antenna_hex_number !== model.antenna_hex_number;
	    });
	  } else {
	    model.id = +new Date();
	    data = this.state.data.slice();
	  }
   
	  this.setState({
	    data: [model, ...data],
   
	  });
	};
   
	onEdit = antenna_hex_number => {
	  let record = this.state.data.find(d => {
	    return d.antenna_hex_number === antenna_hex_number;
	  });
	  //alert(JSON.stringify(record));
	  this.setState({
	    current: record
	  });
	};
   
	onNewClick = e => {
	  this.setState({
	    current: {}
	  });
	};
   
	render() {
	  let data = this.state.data.map(d => {
	    return (
		 <tr key={d.antenna_hex_number}>
		   <td>{d.separation}</td>
		   <td>{d.separation_units}</td>
		   <td>{d.dl}</td>
		   <td>{d.beam}</td>
		   <td>{d.frequency}</td>
		   <td>{d.frequency_units}</td>
		   <td>{d.dish_size}</td>
		   <td>{d.dish_size_units}</td>
		   <td>{d.location}</td>
		 </tr>
	    );
	  });
   
	return (

	  <div className="Home">
	  <DynamicForm
	    className="form"
	    title="21cmSense"
	    defaultValues={this.state.current}
	    model={[
		 { key: "antenna_hex_number", label: "Antena Hex Number", props: { required: true, min: 0} },
		 { key: "separation", label: "Separation", type: "number", props: { required: true, min: 0}},
		 {
		   key: "separtion_units",
		   label: "Separtion Units",
		   type: "radio",
		   options: [
		
			{key: "Mhz", lable: "Mhz", name: "separtion_units", value: "Mhz"},
			{key: "Hz", lable: "Hz", name: "separtion_units", value: "Hz"}
		   ],
		   props: { required: true }
		 },
		 { key: "dl", label: "DL", type: "number", props: { required: true, min: 0}},
		 { key: "frequency", label: "Frequency", type: "number", props: { required: true, min: -180, max: 180}},
		 {
		   key: "frequency_units",
		   label: "Frequency Units",
		   type: "radio",
		   options: [
			{key: "Mhz", lable: "Mhz", name: "frequency_units", value: "Mhz"},
			{key: "Hz", lable: "Hz", name: "frequency_units", value: "Hz"}
		   ],
		   props: { required: true }
		 },
		 { key: "dish_size", label: "Dish Size", type: "number", props: { required: true, min: 0}},
		 {
		   key: "dish_size_units",
		   label: "Dish Size Units",
		   type: "radio",
		   options: [
			
			{key: "mm", lable: "mm", name: "dish_size_units", value: "mm"},
			{key: "cm", lable: "cm", name: "dish_size_units", value: "cm"},
			{key: "m", lable: "m", name: "dish_size_units", value: "m"},
			{key: "km", lable: "km", name: "dish_size_units", value: "km"}
		   ],
		   props: { required: true }
		 }
		 
	    ]}
	    onSubmit={model => {
		 this.onSubmit(model);
	    }}
	  />
   
	  <table border="1">
	    <tbody>{data}</tbody>
	  </table>
	</div>

	);
}
}
export default Home;