import React, {Component} from 'react';

class Login extends Component {

  outerDivStyle = () => {
    return  {"height": "100vh", "display": "flex", "align-items": "center",
    "justify-content": "center"}
  }
  render() {
    return (
        <div style={this.outerDivStyle()}>
        <div className="container" style={{"width":"35%"}}  >
          <div className="jumbotron jumbotron-fluid">
            <div className="container" style={{"textAlign":"center"}}>
              <h1 className="display-4">Welcome to Payroll</h1>
              <p className="lead">Please login or create an account.</p>
            </div>
          </div>
          <form>
            <div className="form-group">
              <label htmlFor="username">Username</label>
              <input type="email" className="form-control" id="username"
                     placeholder="Username"/>
            </div>
            <div className="form-group">
              <label htmlFor="password">Password</label>
              <input type="password" className="form-control" id="password"
                     placeholder="Password"/>
            </div>
            <div className="form-group">
              <br/>
              <button type="submit" className="btn btn-primary">Sign Up</button>
              <button type="submit" className="btn btn-success" style={{"marginLeft":"2%"}}>Login</button>
            </div>
          </form>
        </div>
        </div>
    );
  }
}

export default Login;
