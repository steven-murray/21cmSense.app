import React from "react"
import Navbar from './components/Navbar';
import Home from './components/pages/Home';
import DynamicForm from './components/pages/DynamicForm';
import The21cmSense from "./components/pages/The21cmSense";
import createModel from "./components/pages/createModel";
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
          <Route path='/DynamicForm' component={DynamicForm} />
          <Route path='/Home' component={Home} />
		      <Route path='/createModel' component={createModel} />
        </Switch>
      </Router>
    </>
  );
}


export default App
