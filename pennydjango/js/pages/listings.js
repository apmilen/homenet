import React from 'react'
import ReactDOM from 'react-dom'

import {ListingComponent} from '@/listings/components'
import {FiltersBar} from '@/components/filtersbar'


class Listings extends React.Component {
    constructor(props) {
        super(props)
        this.state = {
            listings: [],
            more_listings_link: null,
        }
    }
    fetchListings(params) {
        $.get(this.props.endpoint, params, (resp) => {
            let fixedLink = null
            if (resp.next !== null) {
                fixedLink = resp.next.slice(0,4) + 's' + resp.next.slice(4)
            }
            this.setState({
                listings: resp.results,
                more_listings_link: fixedLink
            })
        })        
    }
    moreListings() {
        $.get(this.state.more_listings_link, (resp) => {
            let fixedLink = null
            if (resp.next !== null) {
                fixedLink = resp.next.slice(0,4) + 's' + resp.next.slice(4)
            }
            this.setState({
                listings: this.state.listings.concat(resp.results),
                more_listings_link: fixedLink
            })
        })
    }
    render() {
        const {constants} = this.props
        const {listings, more_listings_link} = this.state
        const last_listing = listings.length > 0 && listings.slice(-1)[0]

        const filters = [
            "address", "unit", "sales_agents", "listing_agents", "hoods",
            "price", "price_per_bed", "beds", "baths", "listing_type",
            "listing_id", "size", "pets_allowed", "nofeeonly", "amenities",
            "owner_pays", "exclusive", "vacant", "draft_listings", "date_available"
        ]

        return (
            <div className= "row">
                <div className= "col-12 col-md-10 offset-md-1">
                    <FiltersBar filters={filters}
                                constants={constants}
                                updateParams={::this.fetchListings}
                            />
                    <div className= "card card-small mb-4">
                        <div className= "col">
                            {listings.map(listing => [
                                <ListingComponent key={listing.short_id} listing={listing} constants={constants}/>,
                                listing.short_id != last_listing.short_id &&
                                    <hr key={`${listing.short_id}-hr`} className="divider-hr" />
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
        )
    }
}

ReactDOM.render(
    React.createElement(Listings, global.props),
    global.react_mount,
)
