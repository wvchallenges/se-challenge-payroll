import React, {Component} from 'react';
import axios from "axios";
import * as Constants from '../../constants'
import {withRouter} from "react-router-dom";
import * as Common from '../../common'

class Login extends Component {

  constructor() {
    super();
    this.state = {
      username: "",
      password: "",
      errorMsg: null,
      successMsg: null,
      interMsg: null,
      actionStart: false
    }
  }

  errorHandlerWrapper = (err, url) => {
    const new_state = Common.errorHandler(err, url)
    console.log(this.state)
    this.setState(new_state)
    console.log(this.state)
  }

  handleChange = (e) => {
    this.onClickClearHandler()
    this.setState({[e.target.name]: e.target.value})
  }

  onSubmitSignupHandler = (e) => {
    console.log(e)
    e.preventDefault()
    this.onClickClearHandler()
    if (!(this.state.username && this.state.password)) {
      this.setState({errorMsg: "Please fill in both fields"})
      return
    }
    this.setState({interMsg: "Signing up...", actionStart: true})
    const url = `${Constants.BASE_URL}/signup`
    axios.post(url, {
      username: this.state.username,
      password: this.state.password
    })
    .then(res => {
      this.setState(
          {
            successMsg: res.data.message,
            interMsg: "",
            actionStart: false,
            username: "",
            password: ""
          })
    })
    .catch(err => {
      this.errorHandlerWrapper(err, url)
    })
  }

  onSubmitLoginHandler = (e) => {
    e.preventDefault()
    this.onClickClearHandler()
    if (!(this.state.username && this.state.password)) {
      this.setState({errorMsg: "Please fill in both fields"})
      return
    }
    this.setState({interMsg: "Logging in...", actionStart: true})
    const url = `${Constants.BASE_URL}/login`
    axios.post(url, {}, {
      auth: {
        username: this.state.username,
        password: this.state.password
      },
      withCredentials: true
    })
    .then(res => {
      // window.location.href = "/home"
      window.location.reload()
      this.setState(
          {interMsg: "", successMsg: "Redirecting...", actionStart: false, username: "", password: ""})
    })
    .catch(err => {
      this.errorHandlerWrapper(err, url)
    })
  }

  onSubmitForm = () => {
    console.log("subbmited form")
  }

  onClickClearHandler = () => {
    this.setState({successMsg: "", errorMsg: "", interMsg: ""})
  }


  outerDivStyle = () => {
    return {
      "height": "100vh", "display": "flex", "alignItems": "center",
      "justifyContent": "center"
    }
  }

  render() {
    return (
        <div style={this.outerDivStyle()}>
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
                       onChange={this.handleChange}/>
              </div>
              <div className="form-group">
                <label htmlFor="password">Password</label>
                <input type="password" className="form-control" name="password"
                       placeholder="Password" value={this.state.password}
                       onChange={this.handleChange}/>
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
