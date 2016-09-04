import React from 'react';
import ReactTimeout from 'react-timeout';


class Notifier extends React.Component {

    constructor(props) {
        super(props);
        this.state = {
            notifiers: [],
        }
    }

    render () {
        return (
            <div className="container">
              <div className="well bs-component">
                <legend>Setup Notifier</legend>

                  <p>
                    Once changes on the target page are detected, Kibitzer will compose
                    change report.
                    Choose one or multiple notifiers for sending this report.
                  </p>

                  <div className="checkbox">
                    <label>
                      <input type="checkbox"
                             name="mailgun"
                             ref="mailgun"
                             value="mailgun" />
                      Mailgun &mdash; e-mail <a href="http://www.mailgun.com/">service</a> by
                      RackSpace.
                      (requires registration).
                    </label>
                  </div>

                <div className="form-group" style={{ paddingBottom: '36px' }}>
                    <label htmlFor="python-code" className="control-label">
                        Python script
                    </label>
                    <textarea className="form-control"
                              rows="3"
                              ref="python_code"
                              style={{ fontFamily: 'monospace' }} />
                    <span className="help-block">
                        You have global variable <code>text</code> referencing change report
                        and <code>creds</code> dictionary with contents of <code>kibitzer-creds.yml</code> file.
                    </span>
                </div>

                <div className="form-group" style={{ paddingBottom: '36px' }}>
                    <label htmlFor="bash-code" className="control-label">
                        Bash script
                    </label>
                    <textarea className="form-control"
                              rows="3"
                              ref="bash_code"
                              style={{ fontFamily: 'monospace' }} />
                    <span className="help-block">
                        Change report is passed to <code>stdin</code>.
                    </span>
                </div>

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
        notify: []
    }
    if (this.refs.mailgun.checked) {
        data.notify.push("mailgun");
    }
    if (this.refs.python_code.value != "") {
        data.notify.push({python: this.refs.python_code.value});
    }
    if (this.refs.bash_code.value != "") {
        data.notify.push({bash: this.refs.bash_code.value});
    }
    this.props.saveValues(data)
    this.props.setTimeout(this.props.nextStep, 250);
  }

}

export default ReactTimeout(Notifier)
