import React from 'react';
//import '/App.css';
import Plot from 'react-plotly.js';
import Plotly from 'plotly.js-dist'

function Graph({group,schemaName}) {
    let json;
    let url="http://galileo.sese.asu.edu:8081/schema/"+{group}+"/get/"+{schemaName};
    
    fetch(url).then(function(e){
        return e.json();
    }).then(function(u){
        json=u;
        // if()// add logic to check that the data is of baselines length[x,m] and baselines lenth[y,m]
        {
            var data=[];

            for(let i=0;i<json.x.length;i++)
            {
                data.push({
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
            var layout = {
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
            Plotly.newPlot('myDiv', data, layout);
        }
        // else if()// add logic to the data is of sensitivity
        // {            
        //     var trace1 = {
        //         x: json.x,
        //         y: json.y,
        //         type:'scatter',
        //         line: {
        //             color: 'rgb(55, 128, 191)',
        //             width: 3
        //         }
        //     };
        //     var layout = {
        //         xaxis: {
        //             range: [0,Math.round(Math.max.apply(null,json.x)+1) ],
        //             title:json.xlabel,
        //             showline:true,
        //             linecolor: 'black',
        //             linewidth: 2,
        //             mirror: true
        //         },
        //         yaxis: {
        //             range: [0,Math.round(Math.max.apply(null,json.y)/100)*100],
        //             title:"\u03B4\u0394"+"2".sup()+"21".sub(),showline:true,
        //             linecolor: 'black',
        //             linewidth: 2,
        //             mirror: true
        //         },
        //         title:'Sensitivity Graph',
        //         showlegend:false
        //     };
        //     var data=[trace1];
        //     Plotly.newPlot('myDiv', data, layout); 

        // }
        // else if()//logic for heatmap
        // {
        //     var data=[];
        //     for(i=0;i<json.x.length;i++)
        //     {
        //         data.push({
        //             x:json.x[i],
        //             y:json.y[i],
        //             mode:'markers',
        //             type:'histogram2d',
        //             colorscale : [['0' , 'rgb(0,225,100)'],['1', 'rgb(100,0,200)']],
        //         });
        //     }
        //     var layout = {
        //         xaxis: {
        //             showgrid:true,
        //             showline:true,
        //             linecolor: 'black',
        //             linewidth: 2,
        //             mirror: true,
        //             title:json.xlabel    
        //         },
        //         yaxis: {
        //             showgrid:true,
        //             showline:true,
        //             linecolor: 'black',
        //             linewidth: 2,
        //             mirror: true,
        //             title:json.ylabel
        //         },
        //         title:'Heatmap Graph',
        //         showlegend:false
        //     };
        //     Plotly.newPlot('myDiv', data, layout)
        

        // }
        
    });
	return (
		<div id="myDiv">
	   </div>
	);
}

export default Graph;