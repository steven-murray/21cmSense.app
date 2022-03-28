import React from 'react';
import '../../App.css';
import { Panel } from 'rsuite';
import '../rsuite-default.css';
import { GiInfo, GiPencil, GiEmptyWoodBucket } from "react-icons/gi";
import { Link } from 'react-router-dom';
import '../../TestGraphDownload.js';
import { saveAs } from "file-saver";
import styled from "styled-components";
import Plot from 'react-plotly.js';
import Plotly from 'plotly.js-dist';
// import '../../Graph.js';
// import { Graph } from '../../Graph.js';
//import '../../Graph.js';

/**Reference for graph devolopment DELETE ONCE COMPLETED
 * 1D cut of 2D Sensitivity = Line graph
 * 1D Noise of 2D Sensitivity = Line graph
 * 1D Noise cut of 2D sensitivity = Scatter
 * 1D Sample Variance Cut of 2D Sensitivity = Line graph
 * 2D Sensitivity = Scatter
 * 2D Sensitivity vs k = Scatter
 * 2D Sensitivity vs z = Line graph
 * k vs Redshift Plot = Heatmap
 * Antenna Positions = Line graph
 * Baseline Distributions = Heatmap
 */
import { withCookies, Cookies } from "react-cookie";
import { instanceOf } from "prop-types";


const theme = {
  cyan: {
    default: "#F0FFFF",
    hover: "#00FFFF"
  }
};

const Button = styled.button`
  background-color: ${(props) => theme[props.theme].default};
  color: rgb(128, 0, 0);
  padding: 5px 15px;
  border-radius: 9px;
  &:hover {
    background-color: ${(props) => theme[props.theme].hover};
  }
  &:disabled {
    cursor: default;
    opacity: 0.7;
  }
`;


Button.defaultProps = {
  theme: "cyan"

};

const saveImage = () => {
  saveAs(
    // img_png.attr("src", url),
    // Plotly.toImage(gd,{format:'png',height:400,width:400}),
    "example.png"
  );
};

const saveJSON = () => {
  saveAs(
    "",
    "example.json"
  );
};

const saveCSV = () => {
  saveAs(
    "",
    "example.csv"
  );
};
//{group, schemaName}
// const Graph = ({group, schemaName}) => {
//   let json;
//   group = "calculations"
//   schemaName = "baselines-distributions"
//   let url="http://galileo.sese.asu.edu:8081/api-1.0/schema/"+{group}+"/get/"+{schemaName};
  
//   fetch('http://galileo.sese.asu.edu:8081/api-1.0/schema/'+group+'/get/'+schemaName).then((resplot) => resplot.json())
//   .then((jsonplot) => {

//     json=jsonplot;
//     {
//       var data=[];

//       for(let i=0;i<json.x.length;i++)
//       {
//           data.push({
//               x:json.x[i],
//               y:json.y[i],
//               mode:'markers',
//               type:'scatter',
//               marker:{size:12,symbol:"circle", color:"blue",opacity:0.1,},
//           });
//       }
//       var Xmax=[];
//       var Xmin=[];
//       var Ymax=[];
//       var Ymin=[];
//       json.x.forEach(x=>{
//           Xmax.push(Math.max.apply(null,x));
//           Xmin.push(Math.min.apply(null,x));
//       });
//       json.y.forEach(x=>{
//           Ymax.push(Math.max.apply(null,x));
//           Ymin.push(Math.min.apply(null,x));
//       });
//       var layout = {
//           xaxis: {
//               range: [Math.min.apply(null,Xmin)-10,Math.max.apply(null,Xmax)+10 ],
//               showgrid:false,
//               showline:true,
//               linecolor: 'black',
//               linewidth: 2,
//               mirror: true,
//               zeroline:false,
//               title:json.xlabel    
//           },
//           yaxis: {
//               range: [Math.min.apply(null,Ymin)-10,Math.max.apply(null,Ymax)+10],
//               showgrid:false,
//               showline:true,
//               zeroline:false, 
//               linecolor: 'black',
//               linewidth: 2,
//               mirror: true,
//               title:json.ylabel
//           },
//           title:'BaseLine Graph',
//           showlegend:false
//       };
//       Plot.newPlot('myDiv', data, layout);
//   }
//   });

//   return (
// 		<div id="myDiv">
// 	   </div>,
//        Graph={Graph}
// 	);
          
// };



class The21cmSense extends React.Component {
	
	
	 static propTypes = {
	    cookies: instanceOf(Cookies).isRequired
	  };
	
	constructor(props) {
	    super(props);
		
	    this.state = {
			selectOptions: [],
	     	user:this.props.cookies.get("user") || "",
			LatitudeUnits: '',
			_models:[]
	    }
	  }
	  
	  componentDidMount(){	
		const {user}=this.state;
		if(user !== ""){
		this.getmodels(user);
		}
		
	  }

	  getmodels(uid){
            fetch('http://galileo.sese.asu.edu:8081/api-1.0/users/'+uid+'/models')
                      .then((res) => res.json())
                      .then((json) => {
                          this.setState({
                              _models: json.models
                          });  console.log(json);
                      })		
	  };
	
	handleOnSubmit = (event) => {
		// event.preventDefault();	
			    this.props.history.push({
	      pathname: '/EditModel',
	      state : event
	    });	

	  };
	
	deletemodule(mid){
	    const req = {
	        method: 'DELETE'
			};
	
		    fetch('http://galileo.sese.asu.edu:8081/api-1.0/users/'+this.state.user+'/models/' + mid, req)
				.then(response => {window.location.reload()});
	}

  render() {
	
	  const {_models} = this.state	
	  const resume = _models.map(dataIn => {
      return (
        <div key={dataIn.modelid}>
          {dataIn.modelname}
          <button style={{ float: 'right',  fontSize:18}} title="Delete Model" onClick = {this.deletemodule.bind(this, dataIn.modelid)} > <GiEmptyWoodBucket title = "delete"/>  </button>       
          <button style={{ float: 'right',  fontSize:18}} title="Edit Model" onClick = {this.handleOnSubmit.bind(this, dataIn) } > <GiPencil title = "edit"/>  </button>   
		  
		  </div>
      );
    });
        //{group, schemaName}
    const Graph = (group, schemaName) => {
      let json;
      //let url="http://galileo.sese.asu.edu:8081/api-1.0/schema/"+{group}+"/get/"+{schemaName};
      
      fetch('http://galileo.sese.asu.edu:8081/api-1.0/schema/'+group+'/get/'+schemaName).then((resplot) => resplot.json())
      .then((jsonplot) => {

        json=jsonplot;
        if(schemaName === "baselines-distributions")
        {

          var database=[];

          for(let i=0;i<json.x.length;i++)
          {
              database.push({
                  x:json.x[i],
                  y:json.y[i],
                  mode:'markers',
                  type:'scatter',
                  marker:{size:12,symbol:"circle", color:"blue",opacity:0.1,},
              });
          }
          var Xmax=[];
          var Xmin=[];
          var Ymax=[];
          var Ymin=[];
          json.x.forEach(x=>{
              Xmax.push(Math.max.apply(null,x));
              Xmin.push(Math.min.apply(null,x));
          });
          json.y.forEach(x=>{
              Ymax.push(Math.max.apply(null,x));
              Ymin.push(Math.min.apply(null,x));
          });
          var layoutbase = {
              xaxis: {
                  range: [Math.min.apply(null,Xmin)-10,Math.max.apply(null,Xmax)+10 ],
                  showgrid:false,
                  showline:true,
                  linecolor: 'black',
                  linewidth: 2,
                  mirror: true,
                  zeroline:false,
                  title:json.xlabel    
              },
              yaxis: {
                  range: [Math.min.apply(null,Ymin)-10,Math.max.apply(null,Ymax)+10],
                  showgrid:false,
                  showline:true,
                  zeroline:false, 
                  linecolor: 'black',
                  linewidth: 2,
                  mirror: true,
                  title:json.ylabel
              },
              title:'BaseLine Graph',
              showlegend:false
          };
          Plotly.newPlot('myDiv', database, layoutbase);
      }

        else if(schemaName === '1D-cut-of-2D-sensitivity' || schemaName === '1D-noise-cut-of-2D-sensitivity' || schemaName === '1D-sample-variance-cut-of-2D-sensitivity' || schemaName === '2D-sensitivity' || schemaName === '2D-sensitivity-vs-k' || schemaName === '2D-sensitivity-vs-z')// add logic to the data is of sensitivity
        {            
            var trace1 = {
                x: json.x,
                y: json.y,
                type:'scatter',
                line: {
                    color: 'rgb(55, 128, 191)',
                    width: 3
                }
            };
            var layoutsense = {
                xaxis: {
                    range: [0,Math.round(Math.max.apply(null,json.x)+1) ],
                    title:json.xlabel,
                    showline:true,
                    linecolor: 'black',
                    linewidth: 2,
                    mirror: true
                },
                yaxis: {
                    range: [0,Math.round(Math.max.apply(null,json.y)/100)*100],
                    title:"\u03B4\u0394"+"2".sup()+"21".sub(),showline:true,
                    linecolor: 'black',
                    linewidth: 2,
                    mirror: true
                },
                title:'Sensitivity Graph',
                showlegend:false
            };
            var datasense=[trace1];
            Plotly.newPlot('myDiv', datasense, layoutsense); 

        }
        else if(schemaName === 'k-vs-redshift-plot')//logic for heatmap
        {
            var datak=[];
            for(let i=0;i<json.x.length;i++)
            {
                datak.push({
                    x:json.x[i],
                    y:json.y[i],
                    mode:'markers',
                    type:'histogram2d',
                    colorscale : [['0' , 'rgb(0,225,100)'],['1', 'rgb(100,0,200)']],
                });
            }
            var layoutshift = {
                xaxis: {
                    showgrid:true,
                    showline:true,
                    linecolor: 'black',
                    linewidth: 2,
                    mirror: true,
                    title:json.xlabel    
                },
                yaxis: {
                    showgrid:true,
                    showline:true,
                    linecolor: 'black',
                    linewidth: 2,
                    mirror: true,
                    title:json.ylabel
                },
                title:'Heatmap Graph',
                showlegend:false
            };
            Plotly.newPlot('myDiv', datak, layoutshift)
        

        }
      });

      return (
        <div id="myDiv">
        </div>,
        
          Graph={Graph}
     
      );
              
    };
    Graph("calulation", "k-vs-redshift-plot");
   
    return (
        
        <div>
            <div style={{
              display: 'inline-block', width: 700, paddingLeft: 35
            }}>
              <br></br> 
              <Panel  shaded >
              <label style={{fontWeight: 'bold', fontSize:24, fontFamily: 'Times New Roman'}}> Model <GiInfo title = "create,edit, or delete"/> </label>
              <Link to='/createModel'>
                    <button style={{ float: 'right', fontWeight: 'bold', fontSize:18}} title="New Model" > + </button>
                </Link>
              <br></br><br></br>
                No models created yet. Please click "New Model"<br></br><br></br>
			  <div   style={{color: 'rgb(77, 77, 58)', fontSize:21, fontFamily: 'Rockwell', paddingLeft: 20}}>
		      		 {resume}  
		      </div>	
			  </Panel>
              <br></br>
              <Panel  shaded >
              <label style={{fontWeight: 'bold', fontSize:24, fontFamily: 'Times New Roman'}}> Download Data</label>
              <br></br><br></br>         
        
                <Button onClick={saveJSON} style = {{fontSize:12, fontFamily: 'Rockwell', width:100}}>Download Parameters in JSON</Button>
           
                <Button onClick={saveImage} style = {{fontSize:12, fontFamily: 'Rockwell', width:100}}>Download Image of Graph</Button>
                
                <Button onClick={saveCSV} style = {{fontSize:12, fontFamily: 'Rockwell', width:100}}>Download Graph Data in CSV</Button>
             

  				    <br></br><br></br><br></br>
              
            </Panel>
            </div>

            <div className = "graph">
                <Panel shaded>
                    <label style={{fontWeight: 'bold', fontSize:24, fontFamily: 'Times New Roman'}}> Plot <GiInfo title = "Plots for all created model"/></label>
                    <br></br><br></br>

                    <form>
                        Calculation: <select name = "calculation" id = "calculation">
                        <option value = "" selected = "selected">1D cut of 2D Sensitivity</option>
                        <option value = "" selected = "selected">1D Noise of 2D Sensitivity</option>
                        <option value = "" selected = "selected">1D Noise cut of 2D sensitivity</option>
                        <option value = "" selected = "selected">1D Sample Variance Cut of 2D Sensitivity</option>
                        <option value = "" selected = "selected">2D Sensitivity</option>
                        <option value = "" selected = "selected">2D Sensitivity vs k</option>
                        <option value = "" selected = "selected">2D Sensitivity vs z</option>
                        <option value = "" selected = "selected">k vs Redshift Plot</option>
                        <option value = "" selected = "selected">Antenna Positions</option>
                        <option value = "" selected = "selected">Baseline Distributions</option>
                    </select>
                    </form>
                    <br></br><br></br>
  
                    {/* <Plot
                      data={[
                        {
                          x: [1, 2, 3],
                          y: [2, 6, 3],
                          type: 'scatter',
                          mode: 'lines+markers',
                          marker: {color: 'red'},
                        },
                        {type: 'bar', x: [1, 2, 3], y: [2, 5, 3]},
                      ]}
                      layout={ {width: 320, height: 240, title: 'A Fancy Plot'} }
                    />  */}

                  {/* <div id="myDiv">
                      {/* </div>
                          {/* Graph={Graph} */}
                          {/* <Plot 
                            Graph={Graph}
                          /> */}

                  {/* <div id="myDiv">
                      Graph={Graph}
                  </div> */}

                    <div> 
                    </div>
                    
                </Panel>
            </div>
          
        </div>
      
    );
  }
}
export default withCookies(The21cmSense);
