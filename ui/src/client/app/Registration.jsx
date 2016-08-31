var AccountFields = require('./AccountFields.jsx')
// var SurveyFields  = require('./SurveyFields')
// var Confirmation  = require('./Confirmation')
var Success       = require('./Success.jsx')
import React from 'react';
import _ from 'underscore';


class Registration extends React.Component {

    constructor(props) {
        super(props);
        this.state = {
            step: 1,
            data: {}
        }
    }

    saveValues(data) {
        _.extendOwn(this.state.data, data)
        console.log(this.state.data)
    }

    nextStep() {
        this.setState({
            step: this.state.step + 1
        })
    }

    render () {
        switch (this.state.step) {
            case 1:
                return <AccountFields
                        saveValues={ (data) => this.saveValues(data) }
                        nextStep={ () => this.nextStep() } />
            case 2:
//                return <SurveyFields />
//            case 3:
//                return <Confirmation />
//            case 4:
                return <Success
						email={ this.state.data.email } />
        }
    }
}

module.exports = Registration
