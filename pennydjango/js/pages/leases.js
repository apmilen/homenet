import React from 'react'
import ReactDOM from 'react-dom'


export const Lease = ({lease}) => {
    return <div className="row">
        <div className="col-12">
            <div id="main-listing">
                <div className="container-fluid new-listing-card">
                    <div className="row listing-admin-area">
                        <div className="col-12">
                            <button type="button"
                                    className="btn btn-sm btn-outline-info mr-1">
                                {lease.listing.address}
                            </button>
                            <button type="button"
                                    className="btn btn-sm btn-outline-info mr-1">Manage
                            </button>
                            <button type="button"
                                    className="btn btn-sm btn-outline-info mr-1">Listing
                            </button>
                        </div>
                    </div>
                    <div className="row listing-area-content">
                        <div className="col-lg-4 listing-area-main">
                            <div className="row"
                                 style={{position: 'relative', paddingTop: '56.25%'}}>
                                <a href="{% url 'listings:detail' pk=listing.id %}"
                                   target="_blank" rel="noreferrer noopener">
                                    <img className="lazy img-fluid mx-auto"
                                         src={`${lease.listing.image}`}
                                         width="960"
                                         height="540"
                                         style={{position: 'absolute', top: '0', left: '0', width: '100%', height: '100%'}}/>
                                </a>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
}


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