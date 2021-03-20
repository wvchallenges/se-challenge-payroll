import React, {Component} from 'react';
import axios from "axios";
import * as Constants from '../../constants'
import {withRouter} from "react-router-dom";
import * as Common from '../../common'

class Login extends Component {

  constructor() {
    super();
    // keep track of input fields, http response message types, and whether or not
    // an http request is underway (in which case we show spinning circle)
    this.state = {
      username: "",
      password: "",
      errorMsg: null,
      successMsg: null,
      actionStart: false
    }
  }

  errorHandlerWrapper = (err, url) => {
    // call the common errorHandler and update the state it returns
    // common error handler console logs the appropriate errors
    const new_state = Common.errorHandler(err, url)
    this.setState(new_state)
  }

  onChangeInputHandler = (e) => {
    // bind our inputs to the respective state properties
    // clear all messages
    this.onClickClearHandler()
    this.setState({[e.target.name]: e.target.value})
  }

  onSubmitSignupHandler = (e) => {
    // signup button
    e.preventDefault()
    this.onClickClearHandler()

    // make sure user fills in both fields
    if (!(this.state.username && this.state.password)) {
      this.setState({errorMsg: "Please fill in both fields"})
      return
    }

    // show spinning wheel indicative that we are performing request
    this.setState({actionStart: true})

    // call endpoint
    const url = `${Constants.BASE_URL}/signup`
    axios.post(url, {
      username: this.state.username,
      password: this.state.password
    })
    .then(res => {
      // if successful, show the success message, and stop spinning wheel
      this.setState(
          {
            successMsg: res.data.message,
            actionStart: false,
            username: "",
            password: ""
          })
    })
    .catch(err => {
      // call error function if error occured
      this.errorHandlerWrapper(err, url)
    })
  }

  onSubmitLoginHandler = (e) => {
    // login button
    e.preventDefault()
    this.onClickClearHandler()

    // make sure user fills in both fields
    if (!(this.state.username && this.state.password)) {
      this.setState({errorMsg: "Please fill in both fields"})
      return
    }

    // show spinning wheel indicative that we are performing request
    this.setState({actionStart: true})

    // call endpoint
    const url = `${Constants.BASE_URL}/login`
    axios.post(url, {}, {
      auth: {
        username: this.state.username,
        password: this.state.password
      },
      withCredentials: true
    })
    .then(res => {
      // refresh the window on login, this should redirect us via router
      window.location.reload()
      this.setState(
          {successMsg: "Redirecting...", actionStart: false, username: "", password: ""})
    })
    .catch(err => {
      this.errorHandlerWrapper(err, url)
    })
  }

  onClickClearHandler = () => {
    // if user click clear messages, clear all messages
    this.setState({successMsg: "", errorMsg: ""})
  }

  render() {
    return (
        <div style={Common.outerDivStyle()}>
          <div className="container" style={{"width": "35%"}}>
            <div className="jumbotron jumbotron-fluid">
              <div className="container" style={{"textAlign": "center"}}>
                <h1 className="display-4">Welcome to Payroll</h1>
                <p className="lead">Please login or create an account.</p>
              </div>
            </div>
            <form>
              <div className="form-group">
                <label htmlFor="username">Username</label>
                <input type="text" className="form-control" name="username"
                       placeholder="Username" value={this.state.username}
                       onChange={this.onChangeInputHandler}/>
              </div>
              <div className="form-group">
                <label htmlFor="password">Password</label>
                <input type="password" className="form-control" name="password"
                       placeholder="Password" value={this.state.password}
                       onChange={this.onChangeInputHandler}/>
              </div>
              <div className="form-group">
                <br/>
                <button type="button" className="btn btn-primary"
                        onClick={this.onSubmitSignupHandler}
                        disabled={this.state.actionStart}>Sign Up
                </button>
                <button type="button" className="btn btn-success"
                        style={{"marginLeft": "2%"}}
                        onClick={this.onSubmitLoginHandler}
                        disabled={this.state.actionStart}>Login
                </button>
              </div>
            </form>
            <br/>
            {Common.renderAlert(this.state)}
          </div>
        </div>
    );
  }
}

export default withRouter(Login);
