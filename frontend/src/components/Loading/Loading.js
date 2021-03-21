import React, {Component} from 'react';
import * as Common from "../../common";
import {Link} from "react-router-dom";

class Loading extends Component {
  render() {
    return (
        <div>
          <div style={Common.outerDivStyle()}>
            <div className="container" style={{"width": "35%"}}>
              <div className="jumbotron jumbotron-fluid">
                <div className="container" style={{"textAlign": "center"}}>
                  <h1 className="display-4">Loading...</h1>
                  {/*<p className="lead">Click {<Link to="/">here</Link>} to return*/}
                  {/*  home.</p>*/}
                </div>
              </div>
            </div>
          </div>
        </div>
    );
  }
}

export default Loading;
