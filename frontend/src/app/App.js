import React, {Component} from 'react';
import Navbar from "../components/Navbar/Navbar";

import LoginWrapper from "../components/Login/LoginWrapper";

class App extends Component {
  render() {
    return (
        <div>
          <Navbar/>
          <LoginWrapper/>
        </div>
    );

  }
}

export default App;
