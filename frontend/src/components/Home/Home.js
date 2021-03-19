import React, {Component} from 'react';
import axios from "axios";
const FormData = require('form-data');
const fs = require('fs')


class Home extends Component {

  constructor() {
    super();
    this.state = {
      selectedFile: null,
      uploadedFile: null,
      message: null

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
    })
    .catch(err => {
      this.setState({ uploadedFile: false, message: err.response.data.message })
    })
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





        </div>
    );
  }
}

export default Home;
