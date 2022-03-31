import React, {Component} from 'react';
//import '/App.css';
import Plot from 'react-plotly.js';
import Plotly from 'plotly.js-dist';
// import createPlotlyComponent from "react-plotly.js/factory";

// export function Graph (group,schemaName)  {

        
//         var data=[]
//         var layout = []
//         let json;
//         return (
//         //let url="http://galileo.sese.asu.edu:8081/api-1.0/schema/"+{group}+"/get/"+{schemaName};
        
//         // fetch('http://galileo.sese.asu.edu:8081/api-1.0/schema/'+group+'/get/'+schemaName).then(function(e){ return e.json(); 
//         // }).then((function(u) {

//         fetch('http://galileo.sese.asu.edu:8081/api-1.0/schema/'+group+'/get/'+schemaName).then((resplot) => resplot.json())
//         .then((jsonplot) => {
  
//             json=jsonplot;
//         //json=u;
//         //   if(schemaName === "baselines-distributions")
//         //   {
            
  
//             for(let i=0;i<json.x.length;i++)
//             {
//                 data.push({
//                     x:json.x[i],
//                     y:json.y[i],
//                     mode:'markers',
//                     type:'scatter',
//                     marker:{size:12,symbol:"circle", color:"blue",opacity:0.1,},
//                 });
//             }
//             var Xmax=[];
//             var Xmin=[];
//             var Ymax=[];
//             var Ymin=[];
//             json.x.forEach(x=>{
//                 Xmax.push(Math.max.apply(null,x));
//                 Xmin.push(Math.min.apply(null,x));
//             });
//             json.y.forEach(x=>{
//                 Ymax.push(Math.max.apply(null,x));
//                 Ymin.push(Math.min.apply(null,x));
//             });
//             layout = {
//                 xaxis: {
//                     range: [Math.min.apply(null,Xmin)-10,Math.max.apply(null,Xmax)+10 ],
//                     showgrid:false,
//                     showline:true,
//                     linecolor: 'black',
//                     linewidth: 2,
//                     mirror: true,
//                     zeroline:false,
//                     title:json.xlabel    
//                 },
//                 yaxis: {
//                     range: [Math.min.apply(null,Ymin)-10,Math.max.apply(null,Ymax)+10],
//                     showgrid:false,
//                     showline:true,
//                     zeroline:false, 
//                     linecolor: 'black',
//                     linewidth: 2,
//                     mirror: true,
//                     title:json.ylabel
//                 },
//                 title:'BaseLine Graph',
//                 showlegend:false
//             };
//             Plotly.restyle('myDiv', data, layout);
//         // }
  
//         //   else if(schemaName === '1D-cut-of-2D-sensitivity' || schemaName === '1D-noise-cut-of-2D-sensitivity' || schemaName === '1D-sample-variance-cut-of-2D-sensitivity' || schemaName === '2D-sensitivity' || schemaName === '2D-sensitivity-vs-k' || schemaName === '2D-sensitivity-vs-z')// add logic to the data is of sensitivity
//         //   {            
//         //       var trace1 = {
//         //           x: json.x,
//         //           y: json.y,
//         //           type:'scatter',
//         //           line: {
//         //               color: 'rgb(55, 128, 191)',
//         //               width: 3
//         //           }
//         //       };
//         //       layout = {
//         //           xaxis: {
//         //               range: [0,Math.round(Math.max.apply(null,json.x)+1) ],
//         //               title:json.xlabel,
//         //               showline:true,
//         //               linecolor: 'black',
//         //               linewidth: 2,
//         //               mirror: true
//         //           },
//         //           yaxis: {
//         //               range: [0,Math.round(Math.max.apply(null,json.y)/100)*100],
//         //               title:"\u03B4\u0394"+"2".sup()+"21".sub(),showline:true,
//         //               linecolor: 'black',
//         //               linewidth: 2,
//         //               mirror: true
//         //           },
//         //           title:'Sensitivity Graph',
//         //           showlegend:false
//         //       };
//         //       data=[trace1];
//         //       Plotly.restyle('myDiv', data, layout); 
  
//         //   }
//         //   else if(schemaName === 'k-vs-redshift-plot')//logic for heatmap
//         //   {
          
//         //       for(let i=0;i<json.x.length;i++)
//         //       {
//         //           data.push({
//         //               x:json.x[i],
//         //               y:json.y[i],
//         //               mode:'markers',
//         //               type:'histogram2d',
//         //               colorscale : [['0' , 'rgb(0,225,100)'],['1', 'rgb(100,0,200)']],
//         //           });
//         //       }
//         //       layout = {
//         //           xaxis: {
//         //               showgrid:true,
//         //               showline:true,
//         //               linecolor: 'black',
//         //               linewidth: 2,
//         //               mirror: true,
//         //               title:json.xlabel    
//         //           },
//         //           yaxis: {
//         //               showgrid:true,
//         //               showline:true,
//         //               linecolor: 'black',
//         //               linewidth: 2,
//         //               mirror: true,
//         //               title:json.ylabel
//         //           },
//         //           title:'Heatmap Graph',
//         //           showlegend:false
//         //       };
//         //       Plotly.restyle('myDiv', data, layout)
      
//         //   }
//         }
//         ),
  
        
//         //   <div id="myDiv">
              
//         //   </div>,
//         //   Graph = {Graph}

        
//             /* <Plot data={data} layout={layout}/>
//             {/* {Graph.maps((data, key)=>{
//                     console.log(key);
//                 return(
//                     <div key={key}>
//                     {data.title}
//                     </div>
//                 );
//             })}  */
//             // Plotly.newPlot('myDiv', data, layout)
//             <Plot
//                       data={[
//                         {
//                           x: [1, 2, 3],
//                           y: [2, 6, 3],
//                           type: 'scatter',
//                           mode: 'lines+markers',
//                           marker: {color: 'red'},
//                         },
//                         {type: 'bar', x: [1, 2, 3], y: [2, 5, 3]},
//                       ]}
//                       layout={ {width: 320, height: 240, title: 'A Fancy Plot'} }
//             /> 
//             // <div>
//             // <Plot 
//             // data={this.state.data}
//             // layout={this.state.layout}
//             // onInitialized={(figure) => this.setState(figure)}
//             // onUpdate={(figure) => this.setState(figure)}
//             // />
//             // </div>
//             //Plotly.newPlot('myDiv', data, layout)
//         )
//         //);       
                
//     };

class Graph extends React.Component {
    static propTypes = {
	    cookies: instanceOf(Cookies).isRequired
	  };
	
	 
	 constructor(props) {
	    super(props);
	    this.state = {
			data: [],
			layout: [],
			
			DataisLoaded: false,
			user: this.props.cookies.get("user") || ""
			
	
	    }
	  }
      genertateGraph(group, schemaName){
        fetch('http://galileo.sese.asu.edu:8081/api-1.0/schema/'+group+'/get/'+schemaName).then((resplot) => resplot.json())
        .then((jsonplot) => {
            this.setState({
                data: jsonplot.models,
                layout: jsonplot.layout
            });   console.log(json);
        })	
      }
    

    render(){
        return (
            <div>

            </div>
        );
    }

}

export default Graph;