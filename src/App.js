import React from "react"
import Navbar from './components/Navbar';
import The21cmSense from "./components/pages/The21cmSense";
import createModel from "./components/pages/createModel";
import EditModel from "./components/pages/EditModel";
import "./App.css"
import { BrowserRouter as Router, Switch, Route } from 'react-router-dom';
import './App.css'


function App() {
  return (
    <>
      <Router>
        <Navbar />
        <Switch>
          <Route path='/' exact component={The21cmSense} />
          <Route path='/The21cmSense' component={The21cmSense} />
          <Route path='/createModel' component={createModel} />
		  <Route path='/EditModel' component={EditModel} />  
        </Switch>
      </Router>
    </>
  );
}


export default App
