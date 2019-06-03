import React from 'react'
import ReactDOM from 'react-dom'

import {FiltersBar, ListingComponent} from '@/listings/components'


class Listings extends React.Component {
    constructor(props) {
        super(props)
        this.state = {
            filters: {
                address: '',
                unit: '',
                sales_agents: [],
                listing_agents: [],
                hoods: [],
                price: [],
                price_per_bed: [],
                beds: [],
                baths: [],
                listing_type: 'any',
                listing_id: '',
                size: [],
                pets_allowed: 'any',
                nofeeonly: false,
                amenities: [],
                owner_pays: false,
                exclusive: false,
                vacant: false,
                draft_listings: false,
                date_available: '',
            },
            'listings': [],
        }
    }
    render() {
        const {constants, endpoint} = this.props
        const {listings, filters} = this.state

        return [
            <div className= "row justify-content-center">
                <div className= "p-3">
                    <FiltersBar filters={filters} constants={constants} endpoint={endpoint}
                                updateParentState={new_state => this.setState(new_state)} />
                </div>
            </div>,
            <div className= "row">
                <div className= "col-12 col-md-10 offset-md-1">
                    <div className= "card card-small mb-4">
                        <div className= "col">
                            {listings.map(listing => [
                                <ListingComponent key={listing.short_id} listing={listing} constants={constants}/>,
                                <hr key={`${listing.short_id}-hr`} className= "listings-hr" />
                            ])}
                            {listings.length == 0 &&
                                <center><h4>No listings found! :s</h4></center>
                            }
                        </div>
                    </div>
                </div>
            </div>
        ]
    }
}

ReactDOM.render(
    React.createElement(Listings, global.props),
    global.react_mount,
)
