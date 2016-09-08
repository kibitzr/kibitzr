import React from 'react'
import YAML from 'json2yaml'


class Success extends React.Component {

    render () {
        return (
            <div className="container">
              <div className="well bs-component">
                <legend>Here is your page configuration</legend>
                <p>
                    Now copy-paste it to your <code>kibitzer.yml</code>
                    into <code>pages</code> section.
                </p>
                <pre className='yaml'>
                  {this.yaml_dump(this.props.conf)}
                </pre>
              </div>
            </div>
        )
    }

    yaml_dump (data) {
        let text = YAML.stringify([data]) 
        let lines = text.split('\n');
        lines.splice(0,1);
        return lines.join('\n');
    }

}

export default Success
