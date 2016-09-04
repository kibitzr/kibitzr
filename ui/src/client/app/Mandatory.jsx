import React from 'react';
import ReactTimeout from 'react-timeout';


class Mandatory extends React.Component {

    constructor(props) {
        super(props);
        this.state = {
            name: 'Rocket launches',
            url: 'http://www.nasa.gov/centers/kennedy/launchingrockets/index.html',
        }
    }

    render () {
        return (
            <div className="container">
              <div className="well bs-component">
                <legend>Select target</legend>

                <div className="form-group label-floating">
                    <label className="control-label">Name</label>
                    <input type="text"
                        ref="name"
                        className="form-control"
                        defaultValue={ this.state.name } />
                </div>

                <div className="form-group label-floating">
                    <label className="control-label">URL</label>
                    <input type="text"
                        ref="url"
                        className="form-control"
                        defaultValue={ this.state.url } />
                </div>

                <button className="btn btn-raised btn-primary"
                        onClick={ (e) => this.saveAndContinue(e) }>
                    Save and Continue
                    <div className="ripple-container" />
                </button>

              </div>
            </div>
        )
    }

  saveAndContinue (e) {
    e.preventDefault()
    var data = {
      name: this.refs.name.value,
      url: this.refs.url.value,
    }
    this.props.saveValues(data)
    this.props.setTimeout(this.props.nextStep, 250);
  }
}

export default ReactTimeout(Mandatory)
