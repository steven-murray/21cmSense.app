import React from 'react';
import env from "react-dotenv";
import '../../App.css';
import { Panel } from 'rsuite';
import '../rsuite-default.css';
import { GiInfo, GiPencil, GiEmptyWoodBucket } from "react-icons/gi";
import { Link } from 'react-router-dom';
import '../../TestGraphDownload.js';
import { saveAs } from "file-saver";
import styled from "styled-components";
import Plot from 'react-plotly.js';
import Container from '../elements/ModalContainer';

// import Plotly from 'plotly.js-dist';

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
//   let url=env.REACT_APP_API_URL + "/api-1.0/schema/"+{group}+"/get/"+{schemaName};

//   fetch(env.REACT_APP_API_URL + '/api-1.0/schema/'+group+'/get/'+schemaName).then((resplot) => resplot.json())
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
      user: this.props.cookies.get("user") || "",
      _models: [],
      calc: [],
      pmodel: [],

      HexNumber: '',
      Separation: '',
      DishSize: '',
      Frequency: '',
      Latitude: '',
      SeperationUnits: '',
      DishSizeUnits: '',
      FrequencyUnits: '',
      LatitudeUnits: '',
      data: [{

        x: [
          0.16499818112915432,
          0.21999757483887245,
          0.27499696854859057,
          0.3299963622583087,
          0.38499575596802676,
          0.4399951496777449,
          0.494994543387463,
          0.5499939370971811,
          0.6049933308068992,
          0.6599927245166173,
          0.7149921182263353,
          0.7699915119360535,
          0.8249909056457716,
          0.8799902993554898,
          0.9349896930652078,
          0.9899890867749259,
          1.044988480484644,
          1.0999878741943623,
          1.1549872679040805,
          1.2099866616137984,
          1.2649860553235166,
          1.3199854490332348,
          1.3749848427429527,
          1.429984236452671,
          1.484983630162389,
          1.5399830238721073,
          1.5949824175818252,
          1.6499818112915434,
          1.7049812050012616,
          1.7599805987109796,
          1.8149799924206977,
          1.869979386130416,
          1.9249787798401339,
          1.979978173549852,
          2.03497756725957,
          2.089976960969288,
          2.1449763546790064,
          2.1999757483887246
        ],
        y: [
          12.912515880728177,
          19.45343904564521,
          32.12647074134198,
          53.013664937540476,
          83.31495300123542,
          123.67964944268913,
          175.49621222887464,
          240.19132213905047,
          319.1999168689312,
          413.95492397302746,
          525.8878375169154,
          656.4319695994517,
          807.0276489658172,
          979.0957080145427,
          1174.0676374001425,
          1393.3749279239394,
          1638.449070527133,
          1910.7215562728404,
          2211.628099178302,
          2542.6116481449676,
          2905.0880134032686,
          3300.488686407197,
          3730.2451586434754,
          4195.788921624284,
          4698.551466881734,
          5239.964285963664,
          5821.458870430374,
          6444.466711852103,
          7110.41930180706,
          7820.775293156087,
          8576.945273414734,
          9380.354476553095,
          10232.434394225167,
          11134.61651807939,
          12088.332339759538,
          13095.013350905463,
          14156.091043153674,
          15272.996908137862
        ],
      },
      { type: 'scatter' },
      ],
      layout: { width: 1000, height: 750, title: 'Sensitivity Plot' },
    }

    this.plusSubmit = this.plusSubmit.bind(this);
    this.plot_model = this.plot_model.bind(this)
  }

  componentDidMount() {
    // const modelid = 'b5749a3c-d395-427c-8478-0af262cac35a';
    const { user } = this.state;
    if (user !== "") {
      console.log("YEAH, GETTING MODELS.")
      this.getmodels(user);
      // TODO why do we need to comment this out?
      // This fetch always fails
      // this.getmodel(user, modelid);
    }



    fetch(env.REACT_APP_API_URL + "/api-1.0/schema/calculation")
      .then((res) => res.json())
      .then((json) => {
        this.setState({
          calc: json
        });
      })
  }

  async getmodels(uid) {
    await fetch(env.REACT_APP_API_URL + '/api-1.0/users/' + uid + '/models')
      .then((res) => res.json())
      .then((json) => {
        this.setState({
          _models: json.models
        });
      })
  };

  getmodel(uid, mid) {

    fetch(env.REACT_APP_API_URL + '/api-1.0/users/' + uid + '/models/' + mid)
      .then((res) => res.json())
      .then((json) => {
        this.setState({
          model: json,
          model_id: mid,
          modelName: json.modelname,
          HexNumber: json.data.data.antenna.hex_num,
          Separation: json.data.data.antenna.separation,
          DishSize: json.data.data.beam.dish_size,
          Frequency: json.data.data.beam.frequency,
          Latitude: json.data.data.location.latitude,
          SeperationUnits: json.data.units.antenna.separation,
          DishSizeUnits: json.data.units.beam.dish_size,
          FrequencyUnits: json.data.units.beam.frequency,
          LatitudeUnits: json.data.units.location.latitude
        });
      })
  }

  generateCalcModel(mid) {

    const ml =
    {
      "calculation": "1D-cut-of-2D-sensitivity",
      "data": {
        "antenna": {
          "schema": "hera",
          "hex_num": 7,
          "separation": 14,
          "dl": 12.02
        },
        "beam": {
          "schema": "GaussianBeam",
          "frequency": 100,
          "dish_size": 14
        },
        "location": {
          "schema": "latitude",
          "latitude": 1.382
        }
      },
      "units": {
        "antenna": {
          "hex_num": "m",
          "separation": "m",
          "dl": "m"
        },
        "beam": {
          "frequency": "MHz",
          "dish_size": "m"
        },
        "location": {
          "latitude": "deg"
        }
      }
    }

    const requestmodel = {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(ml)
    };

    fetch(env.REACT_APP_API_URL + '/api-1.0/users/fd1039f8-76b5-495f-9d9b-bbb20520d7b9/models' + mid, requestmodel)
      .then((res) => res.json())
      .then((json) => {
        this.setState({
          pmodel: json
        }); console.log(json)
      })
    console.log(this.state.pmodel);
  }


  handleOnSubmit = (event) => {
    // event.preventDefault();
    this.props.history.push({
      pathname: '/EditModel',
      state: event
    });

  };

  deletemodule(mid) {
    const req = {
      method: 'DELETE'
    };

    fetch(env.REACT_APP_API_URL + '/api-1.0/users/' + this.state.user + '/models/' + mid, req)
      .then(response => { window.location.reload() });
  }

  plusSubmit() {


    console.log("I submitted.");
    const { user } = this.state;

    if (user !== "") {
      this.getmodels(user);
    }
  }

  plot_model(event) {
    console.log(this)
    const requestOptions = {
      method: 'POST',
      headers: { "Content-Type": "application/json" },
    };
    fetch(
      env.REACT_APP_API_URL + "/api-1.0/21cm_default", requestOptions
    ).then(response => response.json()).then(
      values => {
        console.log(values)
        const new_data = [
          {
            x: values.x,
            y: values.y
          },
          { type: "scatter" }
        ];
        this.setState({
          data: new_data
        });
      }
    )





  }

  render() {

    console.log("Re-Rendering", this.state._models);
    const { _models } = this.state

    const resume = _models.map(dataIn => {
      return (
        <div key={dataIn.modelid}  >
          {dataIn.modelname}
          <button style={{ float: 'right', fontSize: 18 }} title="Delete Model" onClick={this.deletemodule.bind(this, dataIn.modelid)} > <GiEmptyWoodBucket title="delete" />  </button>
          <button style={{ float: 'right', fontSize: 18 }} title="Edit Model" onClick={this.handleOnSubmit.bind(this, dataIn)} > <GiPencil title="edit" />  </button>
        </div>
      );
    });



    //{group, schemaName}
    // const Graph = (group, schemaName) => {
    //   let json;
    //   //let url=env.REACT_APP_API_URL + "/api-1.0/schema/"+{group}+"/get/"+{schemaName};

    //   fetch(env.REACT_APP_API_URL + '/api-1.0/schema/'+group+'/get/'+schemaName).then((resplot) => resplot.json())
    //   .then((jsonplot) => {

    //     json=jsonplot;
    //     if(schemaName === "baselines-distributions")
    //     {

    //       var database=[];

    //       for(let i=0;i<json.x.length;i++)
    //       {
    //           database.push({
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
    //       var layoutbase = {
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
    //       Plotly.restyle('myDiv', database, layoutbase);
    //   }

    //     else if(schemaName === '1D-cut-of-2D-sensitivity' || schemaName === '1D-noise-cut-of-2D-sensitivity' || schemaName === '1D-sample-variance-cut-of-2D-sensitivity' || schemaName === '2D-sensitivity' || schemaName === '2D-sensitivity-vs-k' || schemaName === '2D-sensitivity-vs-z')// add logic to the data is of sensitivity
    //     {
    //         var trace1 = {
    //             x: json.x,
    //             y: json.y,
    //             type:'scatter',
    //             line: {
    //                 color: 'rgb(55, 128, 191)',
    //                 width: 3
    //             }
    //         };
    //         var layoutsense = {
    //             xaxis: {
    //                 range: [0,Math.round(Math.max.apply(null,json.x)+1) ],
    //                 title:json.xlabel,
    //                 showline:true,
    //                 linecolor: 'black',
    //                 linewidth: 2,
    //                 mirror: true
    //             },
    //             yaxis: {
    //                 range: [0,Math.round(Math.max.apply(null,json.y)/100)*100],
    //                 title:"\u03B4\u0394"+"2".sup()+"21".sub(),showline:true,
    //                 linecolor: 'black',
    //                 linewidth: 2,
    //                 mirror: true
    //             },
    //             title:'Sensitivity Graph',
    //             showlegend:false
    //         };
    //         var datasense=[trace1];
    //         Plotly.restyle('myDiv', datasense, layoutsense);

    //     }
    //     else if(schemaName === 'k-vs-redshift-plot')//logic for heatmap
    //     {
    //         var datak=[];
    //         for(let i=0;i<json.x.length;i++)
    //         {
    //             datak.push({
    //                 x:json.x[i],
    //                 y:json.y[i],
    //                 mode:'markers',
    //                 type:'histogram2d',
    //                 colorscale : [['0' , 'rgb(0,225,100)'],['1', 'rgb(100,0,200)']],
    //             });
    //         }
    //         var layoutshift = {
    //             xaxis: {
    //                 showgrid:true,
    //                 showline:true,
    //                 linecolor: 'black',
    //                 linewidth: 2,
    //                 mirror: true,
    //                 title:json.xlabel
    //             },
    //             yaxis: {
    //                 showgrid:true,
    //                 showline:true,
    //                 linecolor: 'black',
    //                 linewidth: 2,
    //                 mirror: true,
    //                 title:json.ylabel
    //             },
    //             title:'Heatmap Graph',
    //             showlegend:false
    //         };
    //         Plotly.restyle('myDiv', datak, layoutshift)

    //     }
    //   });

    //   return (
    //     <div id="myDiv">
    //     </div>,
    //     Graph = {Graph}
    //   );

    // };


    return (


      <div>
        <div className="modelStyle">
          <br></br>

          <Panel shaded >
            <label style={{ fontWeight: 'bold', fontSize: 24, fontFamily: 'Times New Roman' }}> Model <GiInfo title="create,edit, or delete" /> </label>
            <Container triggerText="+" onSubmit={this.plusSubmit} buttonClass="btn btn-primary" />
            {/* <button style={{ float: 'right', fontWeight: 'bold', fontSize: 18 }} title="New Model" > + </button> */}
            <br></br><br></br>

            <div style={{ color: 'rgb(77, 77, 58)', fontSize: 21, fontFamily: 'Rockwell', paddingLeft: 50 }}>
              {resume}
            </div>
          </Panel>

          <br></br>

          <Panel shaded >
            <label style={{ fontWeight: 'bold', fontSize: 24, fontFamily: 'Times New Roman' }}> Download Data</label>
            <br></br><br></br>

            <Button onClick={saveJSON} style={{ fontSize: 12, fontFamily: 'Rockwell', width: 100 }}>Download Parameters in JSON</Button>

            <Button onClick={saveImage} style={{ fontSize: 12, fontFamily: 'Rockwell', width: 100 }}>Download Image of Graph</Button>

            <Button onClick={saveCSV} style={{ fontSize: 12, fontFamily: 'Rockwell', width: 100 }}>Download Graph Data in CSV</Button>


            <br></br><br></br><br></br>

          </Panel>
        </div>

        <div className="graph">
          <form >
            <Panel shaded>
              <label style={{ fontWeight: 'bold', fontSize: 24, fontFamily: 'Times New Roman' }}> Plot <GiInfo title="Plots for all created model" /></label>
              <br></br><br></br>
              <label style={{ fontSize: 21, fontFamily: 'Rockwell', width: 100 }}> Calculation </label>
              <select name="Calculation" onChange={this.plot_model} >
                {this.state.calc.map(o => <option value={o.value}>{o}</option>)}
              </select>
              <label style={{ fontSize: 21, fontFamily: 'Rockwell', width: 100 }}> Models </label>
              <select name="models" onChange={this.plot_model}>
                {this.state._models.map(dataIn => <option value={dataIn.modelname}>{dataIn.modelname}</option>)}
              </select>
              <br></br><br></br>

              <Plot
                divId="plotly-div"

                data={this.state.data}
                layout={this.state.layout}


              />

            </Panel>



          </form>
        </div>

      </div>

    );
  }
}
export default withCookies(The21cmSense);
