import React, {Component} from 'react';
import axios from "axios";
import * as Constants from '../../constants'

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

  errorHandler = (err, url) => {
    this.setState({interMsg: "", actionStart: false})
    if (err.response?.status == 404) {
      console.error(err.response.data)
      this.setState({errorMsg: `Could not find URL: ${url}`})
    }
    if (err.response?.data) {
      console.log(`err occured: ${err.response.data.message}`)
      this.setState({errorMsg: err.response.data.message})
    } else {
      console.log(`other type of err ${err}`)
      this.setState({errorMsg: `${err}`})
    }
  }

  handleChange = (e) => {
    this.onClickClearHandler()
    this.setState({[e.target.name]: e.target.value})
  }

  onSubmitSignupHandler = (e) => {
    e.preventDefault()
    if (!(this.state.username && this.state.password)) {
      this.setState({errorMsg: "Please fill in both fields"})
      return
    }
    this.setState({interMsg: "Signing up...", actionStart: true})
    const url = `${Constants.BASE_URL}/signup`
    axios.post(url,{
        username: this.state.username,
        password: this.state.password
    })
    .then(res => {
      this.setState(
          {successMsg: res.data.message, interMsg: "", actionStart: false, username: "", password: ""})
    })
    .catch(err => {
      this.errorHandler(err, url)
    })
    console.log("signup")
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
    axios.post(url,{}, {
      auth: {
        username: this.state.username,
        password: this.state.password
      }
    })
    .then(res => {
      this.setState(
          {interMsg: "", actionStart: false, username: "", password: ""})
    })
    .catch(err => {
      this.errorHandler(err, url)
    })
    console.log("login")
  }

  onClickClearHandler = () => {
    this.setState({successMsg: "", errorMsg: "", interMsg: ""})
  }

  renderAlert() {
    const result = [];
    if (this.state.successMsg) {
      result.push((
          <div className="alert alert-success" role="alert">
            {this.state.successMsg}
          </div>
      ))
    }
    if (this.state.errorMsg) {
      result.push((
          <div className="alert alert-danger" role="alert">
            {this.state.errorMsg}
          </div>
      ))
    }
    if (this.state.interMsg) {
      result.push((
          <div className="d-flex justify-content-center">
            <div className="spinner-border" role="status">
              <span className="sr-only"></span>
            </div>
          </div>
      ))
    }
    return (
        <div>{result}</div>
    )
  }

  outerDivStyle = () => {
    return  {"height": "100vh", "display": "flex", "alignItems": "center",
    "justifyContent": "center"}
  }
  render() {
    return (
        <div style={this.outerDivStyle()}>
        <div className="container" style={{"width":"35%"}}  >
          <div className="jumbotron jumbotron-fluid">
            <div className="container" style={{"textAlign":"center"}}>
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
              <button type="submit" className="btn btn-primary" onClick={this.onSubmitSignupHandler}>Sign Up</button>
              <button type="submit" className="btn btn-success" style={{"marginLeft":"2%"}} onClick={this.onSubmitLoginHandler}>Login</button>
            </div>
          </form>
          <br/>
          {this.renderAlert()}
        </div>
        </div>
    );
  }
}

export default Login;
