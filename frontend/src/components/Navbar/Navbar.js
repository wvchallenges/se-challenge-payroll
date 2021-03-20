import React, {Component} from 'react';

class Navbar extends Component {
  render() {
    return (
        <div>
          <nav className="navbar navbar-light bg-light">
            <div className="container" style={{"textAlign": "center"}}>
              <a className="navbar-brand" href="/#" style={{"width": "100%"}}>
                <img src="/wave.png" alt="" width="30" height="30"
                     style={{"float": "left"}}/>
                Payroll Visualizer
              </a>
            </div>
          </nav>
        </div>
    );
  }
}

export default Navbar;
