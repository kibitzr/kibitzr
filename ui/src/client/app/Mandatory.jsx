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
            <div>
                <label>Name</label> 
                <input type="text"
                     ref="name"
                     defaultValue={ this.state.name } />

                <label>URL</label>
                <input type="text"
                     ref="url"
                     defaultValue={ this.state.url } />

                <button onClick={ (e) => this.saveAndContinue(e) }>
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
