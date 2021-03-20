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

class App extends Component {

  constructor() {
    super();
    this.state = {
      loggedIn: false,
      authenticating: false
    }
  }

  componentDidMount() {
    this.setState({ authenticating: true})
    const url = `${Constants.BASE_URL}/verify`
    axios.get(url,{
      withCredentials: true
    })
    .then(res => {
      this.setState({ loggedIn: true, authenticating: false  })
    })
    .catch(err => {
      this.setState({ loggedIn: false, authenticating: false })
    })
  }

  render() {

    return (
        <div>
          <Navbar/>
          <Router>
            <Switch>
              { !this.state.authenticating ?
                  <React.Fragment>
                    <Route exact path="/home" render={() => this.state.loggedIn ?
                        <Home/> : <Redirect to="/" /> }/>
                    <Route exact path="/" render={() => !this.state.loggedIn ?
                        <Login/> : <Redirect to="/home" /> }/>
                  </React.Fragment> : null
              }
              <Route path="*" render={() => <Redirect to="/"/>}/>


            </Switch>
          </Router>
        </div>
    );

  }
}

export default App;
