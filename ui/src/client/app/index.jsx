import React from 'react';
import {render} from 'react-dom';

import AwesomeComponent from './AwesomeComponent.jsx';
import PageWizard from './PageWizard.jsx';


class App extends React.Component {
  render () {
    return (
      <div>
        <AwesomeComponent />
        <PageWizard />
      </div>
    );
  }
}


render(<App/>, document.getElementById('app'));
