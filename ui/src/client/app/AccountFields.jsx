import React from 'react';

class AccountFields extends React.Component {

	constructor(props) {
		super(props);
		this.state = {
			name: 'Name',
			password: '',
			email: '',
		}
	}

	render () {
		return (
		    <div>
				<label>Name</label> 
				<input type="text"
					 ref="name"
					 defaultValue={ this.state.name } />

				<label>Password</label>
				<input type="password"
					 ref="password"
					 defaultValue={ this.state.password } />

				<label>Email</label>
				<input type="email"
					 ref="email"
					 defaultValue={ this.state.email } />

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
      password: this.refs.password.value,
      email: this.refs.email.value,
    }

    this.props.saveValues(data)
    this.props.nextStep()
  }
}

module.exports = AccountFields
