import React from 'react';

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

                <button className="btn btn-primary"
                        onClick={ (e) => this.saveAndContinue(e) }>
                    Save and Continue
                </button>

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
    this.props.nextStep()
  }
}

module.exports = Mandatory
