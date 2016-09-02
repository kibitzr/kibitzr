import React from 'react';

class Fetcher extends React.Component {

    constructor(props) {
        super(props);
        this.state = {
            format: 'asis',
        }
    }

    render () {
        return (
            <div>
                <label>Fetcher type</label> 

                <select ref="format" defaultValue="asis">
                    <option value="asis">As is</option>
                    <option value="json">JSON</option>
                    <option value="html">HTML using Firefox</option>
                    <option value="text">Text using Firefox</option>
                </select>

                <button onClick={ (e) => this.saveAndContinue(e) }>
                    Save and Continue
                </button>
            </div>
        )
    }

  saveAndContinue (e) {
    e.preventDefault()

    var data = {
      format: this.refs.format.value,
    }

    this.props.saveValues(data)
    this.props.nextStep()
  }
}

module.exports = Fetcher
