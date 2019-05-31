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
        return leases.map(lease =>
            <Lease key={lease.short_id} lease={lease}/>)
    }
}

ReactDOM.render(
    React.createElement(LeasesList, global.props),
    global.react_mount,
)