import '../../App.css';
import React from 'react';
import env from "react-dotenv";
import { Panel } from 'rsuite';
import styled from "styled-components";
import { withCookies, Cookies } from "react-cookie";
import { instanceOf } from "prop-types";

const theme = {
	blue: {
		default: "#9facde",
		hover: "#657aca"
	},
	green: {
		default: "#6ca59b",
		hover: "#6c9ca5"
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
	theme: "green"

};

class CreateModel extends React.Component {

	static propTypes = {
		cookies: instanceOf(Cookies).isRequired
	};


	constructor(props) {
		super(props);
		this.state = {
			modelName: '',
			models: [],
			uid: 'harit',

			HexNumber: '',
			HexType: '',
			HexMin: '',

			Separation: '',
			SepType: '',
			SepMin: '',
			SepEnum: [],

			DishSize: '',
			DSType: '',
			DSMin: '',
			DSEnum: [],

			Frequency: '',
			FreType: '',
			FreMin: '',
			FreEnum: [],

			Latitude: '',
			LaType: '',
			LaMin: '',
			LaMax: '',
			LaEnum: [],

			SeperationUnits: '',
			DishSizeUnits: '',
			FrequencyUnits: '',
			LatitudeUnits: '',

			DataisLoaded: false,
			user: this.props.cookies.get("user") || ""


		}
	}

	componentDidMount() {
		if (document.cookie.indexOf('user') === -1) {
			// this.setState({notice: "I got it"});
			this.generateUserID();

		}

		const { user } = this.state;
		if (user !== "") {
			this.getmodels(user);
		}

		this.getAntennaData();
		this.getBeamData();
		this.getLocationData();
	}

	generateUserID() {
		const { cookies } = this.props;
		const requestOptions = {
			method: 'POST'
		};
		console.log("Generating user ID")
		fetch(env.REACT_APP_API_URL + '/api-1.0/users', requestOptions)
			.then(response => response.json())
			.then((data) => {
				this.setState({
					user: data.uuid
				}, cookies.set("user", data.uuid, { path: "/", maxAge: 130000 }));
			})

		console.log(this.state.user);
	}

	getmodels(uid) {
		fetch(env.REACT_APP_API_URL + '/api-1.0/users/' + uid + '/models')
			.then((res) => res.json())
			.then((json) => {
				this.setState({
					models: json.models
				}); console.log(json);
			})
	}

	async generateModel(uid) {

		const ml = {
			"modelname": this.state.modelName,
			"data": {
				"data": {
					"antenna": {
						"schema": "hera",
						"hex_num": this.state.HexNumber,
						"separation": this.state.Separation
					},
					"beam": {
						"schema": "GaussianBeam",
						"frequency": this.state.Frequency,
						"dish_size": this.state.DishSize
					},
					"location": {
						"schema": "latitude",
						"latitude": this.state.Latitude
					}
				},
				"units": {
					"antenna": {
						"separation": this.state.SeperationUnits
					},
					"beam": {
						"frequency": this.state.FrequencyUnits,
						"dish_size": this.state.DishSizeUnits
					},
					"location": {
						"latitude": this.state.LatitudeUnits
					}
				}
			}
		}

		const requestmodel = {
			method: 'POST',
			headers: { 'Content-Type': 'application/json' },
			body: JSON.stringify(ml)
		};

		const response = await fetch(env.REACT_APP_API_URL + '/api-1.0/users/' + uid + '/models', requestmodel)
		console.log("RESPONSE:", response);
	}

	getAntennaData() {
		fetch(env.REACT_APP_API_URL + "/api-1.0/schema/antenna/get/hera")
			.then((res) => res.json())
			.then((json) => {
				this.setState({
					SeperationUnits: json.units.antenna.separation.default,
					HexType: json.data.antenna.hex_num.type,
					HexMin: json.data.antenna.hex_num.minimum,
					SepType: json.data.antenna.separation.type,
					SepMin: json.data.antenna.separation.minimum,
					SepEnum: json.units.antenna.separation.enum

				});
			})
	}

	getBeamData() {
		console.log("Doing this thing.");
		fetch(env.REACT_APP_API_URL + "/api-1.0/schema/beam/get/GaussianBeam")
			.then((ress) => ress.json())
			.then((jsons) => {
				this.setState({
					FrequencyUnits: jsons.units.beam.frequency.default,
					DishSizeUnits: jsons.units.beam.dish_size.default,
					DSType: jsons.data.beam.dish_size.type,
					DSMin: jsons.data.beam.dish_size.minimum,
					DSEnum: jsons.units.beam.dish_size.enum,
					FreType: jsons.data.beam.frequency.type,
					FreMin: jsons.data.beam.frequency.minimum,
					FreEnum: jsons.units.beam.frequency.enum

				});
			})
		console.log("Done that thing.");
	}

	getLocationData() {
		fetch(env.REACT_APP_API_URL + "/api-1.0/schema/location/get/latitude")
			.then((resss) => resss.json())
			.then((jsonss) => {
				this.setState({
					LatitudeUnits: jsonss.units.location.latitude.default,
					LaType: jsonss.data.location.latitude.type,
					LaMin: jsonss.data.location.latitude.__minimum,
					LaMax: jsonss.data.location.latitude.__maximum,
					LaEnum: jsonss.units.location.latitude.enum,
					DataisLoaded: true
				});
			})
	}

	handleOnSubmit = async (event) => {
		event.preventDefault();
		await this.generateModel(this.state.user);
		this.props.closeModal();
		this.props.onSubmit();
		// this.props.history.push({
		// 	pathname: '/',
		// 	state: this.state
		// });

	};

	handleInputChange = (event) => {
		const { name, value } = event.target;
		this.setState(() => ({

			[name]: value
		}));
	};

	render() {
		console.log(this.state);
		const { DataisLoaded } = this.state;

		if (!DataisLoaded) return <div>
			<br></br>
			<h3 style={{ color: 'rgb(77, 77, 58)', fontFamily: 'Rockwell', paddingLeft: 20 }}> Sorry, we'are unable to reach the server at the moment. Please try again later.. </h3></div>;

		return (
			<form onSubmit={this.handleOnSubmit} >
				<Panel header='ANTENNA' shaded style={{ color: 'rgb(77, 77, 58)', fontSize: 21, fontFamily: 'Rockwell', paddingLeft: 20 }}>
					<label> Hex Number </label>
					<input name="HexNumber" type={this.state.HexType} min={this.state.HexMin} onChange={this.handleInputChange} required />
					<br></br><br></br>
					<label> Separation </label>
					<input name="Separation" type={this.state.SepType} min={this.state.SepMin} onChange={this.handleInputChange} required />
					<select name="SeperationUnits" value={this.state.SeperationUnits} onChange={this.handleInputChange} >
						{this.state.SepEnum.map(o => <option value={o.value}>{o}</option>)}
					</select>
					<br></br><br></br>
				</Panel>
				<Panel header='BEAM' shaded style={{ color: 'rgb(77, 77, 58)', fontSize: 21, fontFamily: 'Rockwell', paddingLeft: 20 }}>
					<label> Dish Size </label>
					<input name="DishSize" type={this.state.DSType} min={this.state.DSMin} onChange={this.handleInputChange} required />
					<select name="DishSizeUnits" value={this.state.DishSizeUnits} onChange={this.handleInputChange} >
						{this.state.DSEnum.map(o => <option value={o.value}>{o}</option>)}
					</select>
					<br></br><br></br>
					<label> Frequency </label>
					<input name="Frequency" type={this.state.FreType} min={this.state.FreMin} onChange={this.handleInputChange} required />
					<select name="FrequencyUnits" value={this.state.FrequencyUnits} onChange={this.handleInputChange} >
						{this.state.FreEnum.map(o => <option value={o.value}>{o}</option>)}
					</select>
					<br></br><br></br>
				</Panel>
				<Panel header='LOCATION' shaded style={{ color: 'rgb(77, 77, 58)', fontSize: 21, fontFamily: 'Rockwell', paddingLeft: 20 }}>
					<label> Latitude </label>
					<input name="Latitude" type={this.state.LaType} min={this.state.LaMin} max={this.state.LaMax} onChange={this.handleInputChange} required />
					<select name="LatitudeUnits" value={this.state.LatitudeUnits} onChange={this.handleInputChange} >
						{this.state.LaEnum.map(o => <option value={o.value}>{o}</option>)}
					</select>
					<br></br><br></br>
				</Panel>
				<br></br><br></br>
				<label style={{ color: 'rgb(128, 0, 0)', fontSize: 18, fontFamily: 'Rockwell', width: 180 }}> Model Name </label>
				<input name="modelName" type={"text"} onChange={this.handleInputChange} required />
				<Button onClick={() => this.props.closeModal()} style={{ fontSize: 24, fontFamily: 'Rockwell', width: 100 }}> Cancel </Button>
				<Button style={{ fontSize: 24, fontFamily: 'Rockwell', width: 100 }} type="submit"
					disabled={this.state.models.some(model => model.modelname === this.state.modelName)}> Save </Button>

			</form>
		);
	}
}

export default withCookies(CreateModel);
