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
            listings: [],
            more_listings_link: null,
        }
    }
    moreListings() {
        $.get(this.state.more_listings_link, (resp) =>
            this.setState({
                listings: this.state.listings.concat(resp.results),
                more_listings_link: resp.next
            })
        )
    }
    render() {
        const {constants, endpoint} = this.props
        const {listings, filters, more_listings_link} = this.state
        const last_listing = listings.length > 0 && listings.slice(-1)[0]

        return [
            <div className="row justify-content-center">
                <div className="m-2 my-md-1 mx-md-5">
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
                                listing.short_id != last_listing.short_id &&
                                    <hr key={`${listing.short_id}-hr`} className= "listings-hr" />
                            ])}
                            {listings.length == 0 ?
                                <center><h4>No listings found</h4></center>
                            :
                                <div className="row justify-content-center">
                                    {more_listings_link ?
                                        <button onClick={::this.moreListings} className="btn btn-outline-primary" style={{padding: 5, margin: 10}}>
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
