import React, {Component} from 'react';
import Navbar from "../components/Navbar/Navbar";

import * as Constants from "../constants";
import axios from "axios";
import {
  BrowserRouter as Router,
  Redirect,
  Route,
  Switch
} from "react-router-dom";
import Home from "../components/Home/Home";
import Login from "../components/Login/Login";
import NoMatch from "../components/NoMatch/NoMatch";
import Loading from "../components/Loading/Loading";

class App extends Component {

  constructor() {
    super();
    // store info about whether we are currently logged in, or trying to check
    this.state = {
      loggedIn: false,
      authenticating: false
    }
  }

  componentDidMount() {
    // when page loads, check to see if we are logged in
    // this verifies the jwt token on the server side
    this.setState({authenticating: true})
    const url = `${Constants.BASE_URL}/verify`
    axios.get(url, {
      withCredentials: true
    })
    .then(res => {
      this.setState({loggedIn: true, authenticating: false})
    })
    .catch(err => {
      this.setState({loggedIn: false, authenticating: false})
    })
  }

  render() {

    return (
        <div>
          <Navbar/>
          <Router>
            <Switch>
              <Route render={({location}) => !['/', '/home'].includes(location.pathname)
                      ? <NoMatch/> :
                      <React.Fragment>
                        {this.state.authenticating ?
                            <Loading/> :
                          <React.Fragment>
                            <Route exact path="/home"
                                   render={() => this.state.loggedIn ?
                                       <Home/> : <Redirect to="/"/>}/>
                            <Route exact path="/"
                                   render={() => !this.state.loggedIn ?
                                       <Login/> : <Redirect to="/home"/>}/>
                          </React.Fragment>
                      }</React.Fragment>
                  }
              />

            </Switch>
          </Router>
        </div>
    );

  }
}

export default App;
