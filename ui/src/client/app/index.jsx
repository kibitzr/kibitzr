import React from 'react';
import {render} from 'react-dom';

import AwesomeComponent from './AwesomeComponent.jsx';
import Registration from './Registration.jsx';


class App extends React.Component {
  render () {
    return (
      <div>
        <p> Hello React!</p>
        <AwesomeComponent />
        <Registration />
      </div>
    );
  }
}


render(<App/>, document.getElementById('app'));
