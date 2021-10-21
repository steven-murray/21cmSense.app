import React from "react"
import Navbar from './components/Navbar';
import Home from './components/pages/Home';
import DecodeJSON from './components/pages/DecodeJSON';
import "./App.css"
import { BrowserRouter as Router, Switch, Route } from 'react-router-dom';
import './App.css'

function App() {
  return (
    <>
      <Router>
        <Navbar />
        <Switch>
          <Route path='/' exact component={Home} />
          <Route path='/DecodeJSON' component={DecodeJSON} />

        </Switch>
      </Router>
    </>
  );
}


export default App
