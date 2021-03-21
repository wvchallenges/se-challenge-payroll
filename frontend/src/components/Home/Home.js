import React, {Component} from 'react';
import axios from "axios";
import Table from "../Table/Table";
import * as Constants from '../../constants'
import * as Common from '../../common'

const FormData = require('form-data');

class Home extends Component {

  constructor() {
    super();
    // keep track of file selected on upload, the report http response message
    // types, and whether or not an http request is underway
    // (in which case we show spinning circle)
    this.state = {
      selectedFile: null,
      report: null,
      toggled: "Show",
      errorMsg: null,
      successMsg: null,
      actionStart: false,
      ref: React.createRef()
    }
  }

  errorHandlerWrapper = (err, url) => {
    // call the common errorHandler and update the state it returns
    // common error handler console logs the appropriate errors
    const new_state = Common.errorHandler(err, url)
    this.setState(new_state)
  }

  onChangeFileHandler = (e) => {
    // user selected csv file, record that in state
    this.setState({selectedFile: e.target.files[0]})
  }

  onSubmitFileHandler = (e) => {
    // user clicks upload on file, now we must process it
    e.preventDefault()
    e.target.value = null;
    let currentRef = this.state.ref;
    currentRef.current.value = "";
    this.setState({ref: currentRef})

    // if file is empty, alert user of this
    if (!this.state.selectedFile) {
      this.setState({successMsg: "", errorMsg: "Please select a file"})
      return;
    }

    // clear all messages off screen when uploading
    this.onClickClearHandler()

    // start creating our http request with form data of the file
    const formData = new FormData()
    formData.append("file", this.state.selectedFile)
    this.setState({ selectedFile: null})

    // show spinning wheel indicative that we are performing request
    this.setState({actionStart: true})

    // call endpoint
    const url = `${Constants.BASE_URL}/upload`
    axios.post(url, formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      },
      withCredentials: true
    }).then(res => {
      this.setState(
          // if successful, show the success message, and stop spinning wheel
          {successMsg: res.data.message, actionStart: false})
      // fetch the report and show the user (even if they don't want to see it)
      this.getReport()
    })
    .catch(err => {
      // call error function if error occured
      this.errorHandlerWrapper(err, url)
    })
  }

  getReport = () => {
    // generate the report
    this.setState({actionStart: true})

    // call endpoint
    const url = `${Constants.BASE_URL}/report`
    axios.get(url, {withCredentials: true})
    .then(res => {
      this.setState(
          // toggle reports button should not say "Hide report"
          {report: res.data, toggled: "Hide", actionStart: false})
    })
    .catch(err => {
      // call error function if error occured
      this.errorHandlerWrapper(err, url)
    })
  }

  onClickToggleHandler = (e) => {
    // if user click toggle report, hide the report, or show it
    if (this.state.toggled === "Hide") {
      this.setState({toggled: "Show"})
      return
    }
    this.getReport()
  }

  onClickLogoutHandler = () => {
    // user clicks logout button
    // show spinning wheel indicative that we are performing request
    this.setState({actionStart: true})

    // call endpoint
    const url = `${Constants.BASE_URL}/logout`
    axios.post(url, {}, {
      withCredentials: true
    }).then(res => {
      this.setState(
          {interMsg: "", errorMsg: "", successMsg: "Redirecting...", actionStart: false})
      // refresh the window on logout, this should redirect us via router
      window.location.reload()

    })
    .catch(err => {
      // call error function if error occured
      this.errorHandlerWrapper(err, url)
    })
  }

  onClickClearHandler = () => {
    // if user click clear messages, clear all messages
    this.setState({successMsg: "", errorMsg: ""})
  }

  render() {
    return (
        <div className="container">
          <br/>
          <button className="btn btn-danger" type="submit"
                  style={{"float": "right"}}
                  onClick={this.onClickLogoutHandler}>Logout
          </button>
          <br/>
          <div className="jumbotron jumbotron-fluid">
            <div className="container" style={{"textAlign": "center"}}>
              <h1 className="display-4">Upload a pay report to get started!</h1>
              <p className="lead">View the report to see a high level
                overview.</p>
            </div>
          </div>
          <br/>
          <form>
            <div className="input-group">
              <input className="form-control" id="formFileLg"
                     type="file" onChange={this.onChangeFileHandler}
              ref={this.state.ref}/>
              <button className="btn btn-primary" type="submit"
                      onClick={this.onSubmitFileHandler}
                      disabled={this.state.actionStart}>Upload
              </button>
            </div>
          </form>
          <br/>
          {Common.renderAlert(this.state)}
          <div className="row" style={{"justifyContent": "center"}}>

            <button className="btn btn-secondary" style={{"width": "25%"}}
                    onClick={this.onClickToggleHandler}
                    disabled={this.state.actionStart}>{this.state.toggled} Report
            </button>

            <button className="btn btn-warning"
                    style={{"width": "25%", "marginLeft": "2%"}}
                    onClick={this.onClickClearHandler}
                    disabled={this.state.actionStart}>Clear Messages
            </button>
          </div>

          {
            this.state.report && this.state.toggled === "Hide" ? <Table
                report={this.state.report}/> : null
          }

        </div>
    );
  }
}

export default Home;
