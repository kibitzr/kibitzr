import React from 'react';

class Fetcher extends React.Component {

    constructor(props) {
        super(props);
        this.state = {
            browser: 'requests',
        }
    }

    render () {
        return (
            <div>
                <h2>Pick fetcher</h2> 
                <div class="description">
                    With the browser you can crop page to one element,
                    wait for Javascript processing, fill up input fields and click buttons.
                    But it works slower.
                </div>

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
