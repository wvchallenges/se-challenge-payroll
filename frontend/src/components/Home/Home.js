import React, {Component} from 'react';
import axios from "axios";
import Table from "../Table/Table";
const FormData = require('form-data');
const fs = require('fs')


class Home extends Component {

  constructor() {
    super();
    this.state = {
      selectedFile: null,
      uploadedFile: null,
      message: null,
      report: null,
      toggled: "Show"
    }
  }

  onChangeHandler = (e) => {
    this.setState({ selectedFile: e.target.files[0]})
    console.log(e.target.files[0])
  }

  onSubmitHandler = (e) => {
    console.log("in submit")
    e.preventDefault()
    if (!this.state.selectedFile) return;


    const formData = new FormData()
    formData.append("file", this.state.selectedFile)
    axios.post('http://127.0.0.1:5000/upload', formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    }).then(res => {
      this.setState({ uploadedFile: true, message: res.data.message })
      this.getReport()
    })
    .catch(err => {
      this.setState({ uploadedFile: false, message: err.response.data.message })
    })
  }

  getReport = () => {
    axios.get('http://127.0.0.1:5000/report')
    .then(res => {
      this.setState({report: res.data, toggled: "Hide"})
      // this.setState({ uploadedFile: true, message: res.data.message })
    })
    .catch(err => {
      console.error(err)
      // this.setState({ uploadedFile: false, message: err.response.data.message })
    })
  }

  onClickToggleHandler = (e) => {
    console.log("in on toggle")
    if (this.state.toggled == "Hide") {
      this.setState({toggled: "Show"})
      return
    }
    this.getReport()

  }

  renderAlert() {
    if (this.state.uploadedFile !== null) {
      if (this.state.uploadedFile) {
        return (
            <div className="alert alert-success" role="alert">
              {this.state.message}
            </div>
        )
      } else {
        return (
            <div className="alert alert-danger" role="alert">
              {this.state.message}
            </div>
        )
      }
    }
  }

  render() {
    return (
        <div className="container">
          <br/>
          <form>
            <label htmlFor="formFileLg" className="form-label">Upload an pay report file</label>
            <div className="input-group">
              <input className="form-control" id="formFileLg"
                     type="file" onChange={this.onChangeHandler}/>
              <button className="btn btn-primary" type="submit" onClick={this.onSubmitHandler}>Upload
              </button>
            </div>
          </form>
          <br/>
          {this.renderAlert()}
          <button className="btn btn-secondary" onClick={this.onClickToggleHandler}>{this.state.toggled} Report</button>
          {
            this.state.report && this.state.toggled == "Hide" ? <Table report={this.state.report}/> : null
          }





        </div>
    );
  }
}

export default Home;
