import React from "react"
import Navbar from './components/Navbar';
import Home from './components/pages/Home';
import DECODE from './components/pages/DECODE';
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
          <Route path='/DECODE' component={DECODE} />

        </Switch>
      </Router>
    </>
  );
}


export default App
