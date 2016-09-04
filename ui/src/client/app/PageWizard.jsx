import Mandatory from './Mandatory.jsx'
import Fetcher from './Fetcher.jsx'
import Browser from './Browser.jsx'
import Notifier from './Notifier.jsx'
import Success from './Success.jsx'
import React from 'react';
import _ from 'underscore';


class PageWizard extends React.Component {

    constructor(props) {
        super(props);
        this.state = {
            step: 4,
            data: {}
        }
    }

    saveValues(data) {
        _.extendOwn(this.state.data, data)
        console.log(this.state.data)
    }

    nextStep() {
        let increment = 1
        if (this.state.step == 2 && this.state.data.fetcher == 'requests') {
            increment = 2
        }
        this.setState({
            step: this.state.step + increment
        })
    }

    render () {
        switch (this.state.step) {
            case 1:
                return <Mandatory
                        saveValues={ (data) => this.saveValues(data) }
                        nextStep={ () => this.nextStep() } />
            case 2:
                return <Fetcher
                        saveValues={ (data) => this.saveValues(data) }
                        nextStep={ () => this.nextStep() } />
            case 3:
                return <Browser
                        saveValues={ (data) => this.saveValues(data) }
                        nextStep={ () => this.nextStep() } />
            case 4:
                return <Notifier
                        saveValues={ (data) => this.saveValues(data) }
                        nextStep={ () => this.nextStep() } />
            case 5:
                return <Success
						email={ this.state.data.email } />
        }
    }
}

module.exports = PageWizard
