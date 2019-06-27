import React from 'react'
import ReactDOM from 'react-dom'

import {Lease} from '@/leases/components'
import {FiltersBar} from '@/components/filtersbar'

export class LeasesList extends React.PureComponent {
    constructor(props) {
        super(props)
        this.state = {
            leases: [],
            more_leases_link: '',
        }
    }
    fetchLeases(params) {
        $.get(this.props.endpoint, params, response => {
            this.setState({
                leases: response.results,
                more_leases_link: response.next
            })
        })
    }
    moreLeases() {
        $.get(this.state.more_leases_link, response => {
            this.setState({
                leases: this.state.leases.concat(response.results),
                more_leases_link: response.next
            })
        })
    }

    render() {
        const {constants} = this.props
        const {leases, more_leases_link} = this.state
        const last_lease = leases.length > 0 && leases.slice(-1)[0]

        const filters = [
            "address", "unit", "sales_agents", "listing_agents", "hoods",
            "price", "beds", "lease_id"
        ]

        return [
            <FiltersBar filters={filters}
                        constants={constants}
                        updateParams={::this.fetchLeases}
                    />,
            leases.map(lease => [
                <Lease key={lease.short_id} lease={lease}/>,
                lease.short_id != last_lease.short_id &&
                    <hr key={`${lease.short_id}-hr`} className="divider-hr" />
            ]),
            leases.length == 0 ?
                <center><h4>No leases found</h4></center>
            :
                <div className="row justify-content-center">
                    {more_leases_link ?
                        <button onClick={::this.moreLeases} className="btn btn-outline-primary" style={{padding: 5, margin: 10}}>
                            Load more...
                        </button>
                    :
                        <div style={{width: '100%', height: 30, textAlign: 'center'}}>
                            <div style={{borderBottom: '1px solid gray', height: 12, width: '95%', margin: 'auto'}}>
                                <span style={{fontSize: '1em', backgroundColor: 'white', padding: '0 10px'}}>
                                    End of results
                                </span>
                            </div>
                        </div>
                    }
                </div>
        ]
    }
}

ReactDOM.render(
    React.createElement(LeasesList, global.props),
    global.react_mount,
)