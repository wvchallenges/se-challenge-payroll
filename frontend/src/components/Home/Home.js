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
      toggled: "Show",
      errorMsg: null,
      successMsg: null
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
    this.setState({successMsg: "", errorMsg: ""})


    const formData = new FormData()
    formData.append("file", this.state.selectedFile)
    axios.post('http://127.0.0.1:5000/upload', formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    }).then(res => {
      this.setState({ successMsg: res.data.message })
      this.getReport()
    })
    .catch(err => {
      if (err.response?.data) {
        console.log(`err occured: ${err.response.data.message}`)
        this.setState({ errorMsg: err.response.data.message})
      } else {
        console.log(`other type of err ${err}`)
        this.setState({ errorMsg: `${err}` })
      }
    })
  }

  getReport = () => {
    axios.get('http://127.0.0.1:5000/report')
    .then(res => {
      this.setState({report: res.data, toggled: "Hide"})
      // this.setState({ uploadedFile: true, message: res.data.message })
    })
    .catch(err => {
      console.log(`err is ${err}`)
      if (err.response?.data) {
        this.setState({ successMsg: err.response.data.message})
      } else {
        console.log(`other type of err ${err}`)
        this.setState({ errorMsg: `${err}` })
      }
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
    return (
        <div>{result}</div>
    )
  }

  onClickClearHandler = () => {
    this.setState({successMsg: "", errorMsg: ""})
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
          <div className="row" style={{"justifyContent":"center"}}>

            <button className="btn btn-secondary" style={{"width":"25%"}} onClick={this.onClickToggleHandler}>{this.state.toggled} Report</button>

            <button className="btn btn-warning" style={{"width":"25%", "marginLeft":"2%"}} onClick={this.onClickClearHandler}>Clear Messages</button>
          </div>


          {
            this.state.report && this.state.toggled == "Hide" ? <Table report={this.state.report}/> : null
          }






        </div>
    );
  }
}

export default Home;
