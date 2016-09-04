import React from 'react';
import ReactTimeout from 'react-timeout';


class Fetcher extends React.Component {

    constructor(props) {
        super(props);
        this.state = {
            fetcher: 'requests',
        }
    }

    render () {
        return (
            <div className="container">
              <div className="well bs-component">
                <legend>Choose HTTP fetcher</legend>
                <div className="form-group">

                  <div className="radio">
                    <label>
                      <input type="radio"
                             name="fetcher"
                             ref="fetcher"
                             value="requests" />
                      <span className="circle"></span><span className="check"></span>
                      <b>requests.get</b> &mdash;
                      Fast and simple.
                      Good for APIs and small text pages without JavaScript.
                    </label>
                  </div>

                  <div className="radio">
                    <label>
                      <input type="radio"
                             name="fetcher"
                             ref="fetcher"
                             value="browser" />
                      <span className="circle"></span><span className="check"></span>
                      <b>Firefox</b> &mdash;
                      Full power of a modern web browser.<br />
                      You will be able to script user interactions,
                      process JavaScript and filter contents by tag name or X-Path.
                    </label>
                  </div>

                <button className="btn btn-raised btn-primary"
                        onClick={ (e) => this.saveAndContinue(e) }>
                    Save and Continue
                </button>

            </div>
          </div>
        </div>
        )
    }

  saveAndContinue (e) {
    e.preventDefault()

    var data = {
      fetcher: this.refs.fetcher.value,
    }

    this.props.saveValues(data)
    this.props.setTimeout(this.props.nextStep, 250);
  }
}

export default ReactTimeout(Fetcher)
