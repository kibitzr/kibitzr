import React from 'react';
import {render} from 'react-dom';

import AwesomeComponent from './AwesomeComponent.jsx';
import PageWizard from './PageWizard.jsx';

import "bootstrap-webpack";
import "bootstrap/dist/css/bootstrap.css";
import "bootstrap-material-design/dist/css/ripples.css";
import "bootstrap-material-design/dist/css/bootstrap-material-design.css";
import "bootstrap-material-design/dist/js/material.js";
import 'bootstrap-material-design/dist/js/ripples.js';

import $ from 'jquery';

class App extends React.Component {
  render () {
    return (
      <div className="container">
        <h1>Kibitzer Configuration Wizard</h1>
        <PageWizard />
      </div>
    );
  }
}

$(() => {
	$.material.init();
});


render(<App/>, document.getElementById('app'));
