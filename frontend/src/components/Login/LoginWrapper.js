import React, {Component} from 'react';
import Home from "../Home/Home";
import Login from "./Login";
import { BrowserRouter as Router, Route, Switch, Redirect, withRouter } from "react-router-dom";
import axios from "axios";
import * as Constants from "../../constants";

class LoginWrapper extends Component {

  constructor() {
    super();
    this.state = {
      loggedIn: false
    }
  }

  checkToken = () => {
    const url = `${Constants.BASE_URL}/verify`
    axios.get(url,{
        withCredentials: true
      })
    .then(res => {
      this.setState({ loggedIn: true })
    })
    .catch(err => {
      this.setState({ loggedIn: false })
    })
  }

  componentDidMount() {
    console.log("checking")
    this.checkToken()
  }

  render() {
    return (
        <Router>
          <Switch>
            <Route path="/home" render={() => this.state.loggedIn ?
                <Home/> : <Redirect to="/" /> }/>
            <Route path="/" render={() => !this.state.loggedIn ?
                    <Login/> : <Redirect to="/home" /> }/>
          </Switch>
        </Router>
    );
  }
}

export default LoginWrapper;
