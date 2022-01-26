import React from "react"
import Navbar from './components/Navbar';
import Home from './components/pages/Home';
import DynamicForm from './components/pages/DynamicForm';
import the21cmSense from "./components/pages/the21cmSense";
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
          <Route path='/The21cmSense' component={the21cmSense} />
          <Route path='/DynamicForm' component={DynamicForm} />
        </Switch>
      </Router>
    </>
  );
}


export default App
