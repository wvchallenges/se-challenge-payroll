import React, {Component} from 'react';
import Navbar from "../components/Navbar/Navbar";
import Home from "../components/Home/Home";
import Login from "../components/Login/Login";

class App extends Component {
  render() {
    return (
        <div>
          <Navbar/>
          <Login/>

          {/*<Home/>*/}



        </div>
    );
  }
}

export default App;
