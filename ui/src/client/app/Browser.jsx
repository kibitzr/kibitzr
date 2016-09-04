import React from 'react';
import ReactTimeout from 'react-timeout';


class Browser extends React.Component {

    constructor(props) {
        super(props);
        this.state = {
            scenario: null,
            xpath: null,
            tag: null,
        }
    }

    render () {
        return (
            <div className="container">
              <div className="well bs-component">
                <legend>Setup Firefox fetcher</legend>

                <div className="form-group" style={{ paddingBottom: '36px' }}>
                    <label htmlFor="scenario" className="control-label">
                        Selenium scenario
                    </label>
                    <textarea className="form-control"
                              rows="7"
                              ref="scenario"
                              style={{ fontFamily: 'monospace' }} />
                    <span className="help-block">
                        It is regular Python script.
                        You have global variable <code>driver</code> which
                        references <a href="http://selenium-python.readthedocs.io/api.html">
                            Selenium Firefox webdriver
                        </a>.<br />
                        It will be executed right after target page is loaded.
                        Leave this field blank if no user interactions are required.
                    </span>
                </div>

                <p>
                    You can filter page HTML contents using one the following locator types.
                    By first occurence of a tag name,
                    or by its <a href="https://en.wikipedia.org/wiki/XPath">XPath</a>. 
                </p>

                <div className="form-group label-floating">
                    <label className="control-label">Tag</label>
                    <input type="text"
                        ref="tag"
                        className="form-control"
                        defaultValue={ this.state.tag } />
                </div>

                <p>
                    If both fields are filled, Tag will be ignored and XPath used.
                </p>

                <div className="form-group label-floating">
                    <label className="control-label">X-Path</label>
                    <input type="text"
                        ref="xpath"
                        className="form-control"
                        defaultValue={ this.state.xpath } />
                </div>

                <p>
                    While writing XPath can be hard, you can use your browser's
                    developer tools:
                </p>
                <ol>
                    <li>Right click page element;</li>
                    <li>From drop-down menu choose <i>Inspect</i>;</li>
                    <li>In opened Elements browser right click on a code of the element;</li>
                    <li>Choose <i>Copy XPath</i>.</li>
                </ol>

                <button className="btn btn-raised btn-primary"
                        onClick={ (e) => this.saveAndContinue(e) }>
                    Save and Continue
                </button>

            </div>
          </div>
        )
    }

  saveAndContinue (e) {
    e.preventDefault()
    var data = {
      scenario: this.refs.scenario.value,
      tag: this.refs.tag.value,
      xpath: this.refs.xpath.value,
    }
    this.props.saveValues(data)
    this.props.setTimeout(this.props.nextStep, 250);
  }

}

export default ReactTimeout(Browser)
