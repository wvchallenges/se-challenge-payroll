import React, {Component} from 'react';

class Home extends Component {

  constructor() {
    super();
    this.state = {
      selectedFile: null
    }
  }

  onChangeHandler = (e) => {
    this.setState({ selectedFile: e.target.files[0]})
  }
  render() {
    return (
        <div className="container">
          <br/>
          <div>
            <label htmlFor="formFileLg" className="form-label">Upload an pay report file</label>
            <input className="form-control form-control-lg" id="formFileLg"
                   type="file" onChange={this.onChangeHandler}/>
          </div>
          {this.state['selectedFile'] ? this.state.selectedFile.name : ""}

        </div>
    );
  }
}

export default Home;
