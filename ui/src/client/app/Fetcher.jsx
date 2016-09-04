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
            <div className="form-group">

                  <div className="radio">
                    <label>
                      <input type="radio"
                             name="format"
                             ref="format"
                             value="asis" />
                      <span className="circle"></span><span className="check"></span>
                      As is
                    </label>
                  </div>

                  <div className="radio">
                    <label>
                      <input type="radio"
                             name="format"
                             ref="format"
                             value="json" />
                      <span className="circle"></span><span className="check"></span>
                      JSON
                    </label>
                  </div>

                  <div className="radio">
                    <label>
                      <input type="radio"
                             ref="format"
                             name="format"
                             value="html" />
                      <span className="circle"></span><span className="check"></span>
                      HTML using Firefox
                    </label>
                  </div>
                  <div className="radio">
                    <label>
                      <input type="radio"
                             ref="format"
                             name="format"
                             value="text" />
                      <span className="circle"></span><span className="check"></span>
                      Text using Firefox
                    </label>
                  </div>

                <button className="btn btn-raised btn-primary"
                        onClick={ (e) => this.saveAndContinue(e) }>
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
    this.props.setTimeout(this.props.nextStep, 250);
  }
}

export default ReactTimeout(Mandatory)
