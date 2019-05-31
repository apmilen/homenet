import React from 'react'
import ReactDOM from 'react-dom'

import {Lease} from '@/leases/components'

export class LeasesList extends React.PureComponent {
    constructor(props) {
        super(props)
        this.state = {
            leases: []
        }
    }
    componentDidMount() {
        $.get(this.props.endpoint, response => {
            console.log(response)
            this.setState({leases: response.results})
        })
    }

    render() {
        let leases = this.state.leases
        return <div className="row">
            <div className="col-12 col-md-10 offset-md-1">
                <div className="card card-small mb-4">
                    <div className="col">
                        {leases.map(lease =>
                            <Lease key={lease.short_id} lease={lease}/>)}
                    </div>
                </div>
            </div>
        </div>
    }
}

ReactDOM.render(
    React.createElement(LeasesList, global.props),
    global.react_mount,
)