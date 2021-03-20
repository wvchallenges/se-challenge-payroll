import React, {Component} from 'react';
import axios from "axios";
import Table from "../Table/Table";
import * as Constants from '../../constants'

const FormData = require('form-data');

class Home extends Component {

  constructor() {
    super();
    this.state = {
      selectedFile: null,
      report: null,
      toggled: "Show",
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

  onChangeFileHandler = (e) => {
    this.setState({selectedFile: e.target.files[0]})
  }

  onSubmitFileHandler = (e) => {
    e.preventDefault()
    e.target.value = null;
    if (!this.state.selectedFile) {
      return;
    }
    const formData = new FormData()

    formData.append("file", this.state.selectedFile)
    this.onClickClearHandler()
    this.setState({interMsg: "Attempting to upload...", actionStart: true})

    const url = `${Constants.BASE_URL}/upload`
    axios.post(url, formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      },
      withCredentials: true
    }).then(res => {
      this.setState(
          {successMsg: res.data.message, interMsg: "", actionStart: false})
      this.getReport()
    })
    .catch(err => {
      this.errorHandler(err, url)
    })
  }

  getReport = () => {
    this.setState({interMsg: "Fetching report...", actionStart: true})
    const url = `${Constants.BASE_URL}/report`
    axios.get(url, {withCredentials: true})
    .then(res => {
      this.setState(
          {report: res.data, toggled: "Hide", interMsg: "", actionStart: false})
    })
    .catch(err => {
      this.errorHandler(err, url)
    })
  }

  onClickToggleHandler = (e) => {
    if (this.state.toggled == "Hide") {
      this.setState({toggled: "Show"})
      return
    }
    this.getReport()
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

  onClickClearHandler = () => {
    this.setState({successMsg: "", errorMsg: "", interMsg: ""})
  }

  render() {
    return (
        <div className="container">
          <br/>
          <form>
            <label htmlFor="formFileLg" className="form-label">Upload an pay
              report file</label>
            <div className="input-group">
              <input className="form-control" id="formFileLg"
                     type="file" onChange={this.onChangeFileHandler}/>
              <button className="btn btn-primary" type="submit"
                      onClick={this.onSubmitFileHandler}
                      disabled={this.state.actionStart}>Upload
              </button>
            </div>
          </form>
          <br/>
          {this.renderAlert()}
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
            this.state.report && this.state.toggled == "Hide" ? <Table
                report={this.state.report}/> : null
          }


        </div>
    );
  }
}

export default Home;
