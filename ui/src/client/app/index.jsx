import React from 'react';
import {render} from 'react-dom';

import AwesomeComponent from './AwesomeComponent.jsx';
import PageWizard from './PageWizard.jsx';

global.jQuery = require('jquery');
require("bootstrap-webpack");


class App extends React.Component {
  render () {
    return (
      <div className="container">
        <AwesomeComponent />
        <PageWizard />
      </div>
    );
  }
}


render(<App/>, document.getElementById('app'));
