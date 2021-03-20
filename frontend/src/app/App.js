import React, {Component} from 'react';
import Navbar from "../components/Navbar/Navbar";

import LoginWrapper from "../components/Login/LoginWrapper";
import { BrowserRouter as Router, Route, Switch } from "react-router-dom";

class App extends Component {
  render() {
    return (
        <div>
          <Navbar/>
          <Router>
            <Switch>
            <Route path="/" component={LoginWrapper}/>
            </Switch>
          </Router>
        </div>
    );

  }
}

export default App;
