import React, {Component} from 'react';
import * as Common from "../../common";

class Loading extends Component {
  render() {
    return (
        <div>
          <div style={Common.outerDivStyle()}>
            <div className="container" style={{"width": "35%"}}>
              <div className="jumbotron jumbotron-fluid">
                <div className="container" style={{"textAlign": "center"}}>
                  <h1 className="display-4">Loading...</h1>
                </div>
              </div>
            </div>
          </div>
        </div>
    );
  }
}

export default Loading;
