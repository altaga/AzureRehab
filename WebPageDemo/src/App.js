import React, { Component } from 'react';
import WebcamComponent from "./cam"

class App extends Component {
  callback = (childData) => {
    console.log(childData)
  }

  render() {
    return (
      <div>
        <WebcamComponent
          captureElement={this.callback}
        />
      </div>
    );
  }
}

export default App;
