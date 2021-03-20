import React, {Component} from 'react';
import {Link} from 'react-router-dom';
import * as Common from '../../common'

class NoMatch extends Component {

  render() {
    return (
        <div style={Common.outerDivStyle()}>
          <div className="container" style={{"width": "35%"}}>
            <div className="jumbotron jumbotron-fluid">
              <div className="container" style={{"textAlign": "center"}}>
                <h1 className="display-4">404. Path Not Found</h1>
                <p className="lead">Click {<Link to="/">here</Link>} to return
                  home.</p>
              </div>
            </div>
          </div>
        </div>
    );
  }
}

export default NoMatch;
