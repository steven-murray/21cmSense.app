import React from "react"
import Navbar from './components/Navbar';
import Home from './components/pages/Home';
import DynamicForm from './components/pages/DynamicForm';
import Prototype from "./components/pages/21cmSense";
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
          <Route path='/Prototype' component={Prototype} />
          <Route path='/DynamicForm' component={DynamicForm} />
        </Switch>
      </Router>
    </>
  );
}


export default App
