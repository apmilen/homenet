import React from 'react'
import ReactDOM from 'react-dom'

import Dropdown from "react-bootstrap/Dropdown";
import Row from "react-bootstrap/Row";
import Col from "react-bootstrap/Col";
import Button from "react-bootstrap/Button";
import differenceInDays from "date-fns/difference_in_days";

import {tooltip} from '@/util/dom'

import {FiltersBar} from '@/components/filtersbar'
import {MapComponent, coordinates} from '@/components/maps'
import {Switch, SettingsGear} from '@/components/misc'


const ListingGrid = ({listing, hoverOn}) => {
    const listing_existance = differenceInDays(Date.now(), listing.created)
    const new_listing = listing_existance < 1 ? 'New Listing' : ''

    return (
        <div className="col-lg-6 col-md-12 mx-w-450 px-1 card card-smallcard-post card-post--1 card-listing overlay-parent"
             onMouseEnter={() => {hoverOn(listing)}} onMouseLeave={() => {hoverOn(undefined)}}>
            <a className="overlay" href={listing.listing_link} target="_blank"></a>
            <div className="card-post__image text-center">
                <img className="box-wd" src={listing.default_image} />
                {listing.no_fee_listing &&
                    <span className="card-post__category left-badge badge badge-pill badge-info">no fee</span>
                }
                <span className="card-post__category new-listing-badge badge badge-pill badge-success">{new_listing}</span>
                <span className="card-post__category badge badge-pill badge-dark">${listing.price}</span>
            </div>
            <div className="card-body p-0 text-center">
                <table className="table mb-0 listing-info">
                    <tbody>
                        <tr>
                            <td className="wrap-info"
                                {...tooltip(`${listing.bedrooms} Beds / ${listing.baths} Bath`)}>
                                {parseFloat(listing.bedrooms).toString()} Beds / {parseFloat(listing.bathrooms).toString()} Bath
                            </td>
                            <td className="wrap-info" colSpan="2"
                                {...tooltip(listing.address)}>
                                {listing.neighborhood}
                            </td>
                        </tr>
                        <tr>
                            <td className="wrap-info">{listing.pets}</td>
                            <td className="wrap-info">
                                <i className="material-icons">share</i> Share
                            </td>
                            <td className="wrap-info">
                                <i className="material-icons">place</i>Map
                            </td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </div>
    )
}


const ListingList = ({listing, hoverOn}) => (
    <div className="card col-11 col-md-12 col-lg-11 col-xl-10 px-0 mx-auto my-1 overlay-parent"
         onMouseEnter={() => {hoverOn(listing)}} onMouseLeave={() => {hoverOn(undefined)}}>
        <a className="overlay" href={listing.listing_link} target="_blank"></a>
        <div className="d-flex align-items-center">

            <div className="">
                <img height="60" width="100"
                     style={{borderRadius: '.625rem 0 0 .625rem'}}
                     src={listing.default_image} />
            </div>

            <div className="col text-center">
                {parseFloat(listing.bedrooms).toString()} Beds<br/>
                {parseFloat(listing.bathrooms).toString()} Baths
            </div>
            <div className="col d-none d-sm-inline" {...tooltip(listing.address)}>{listing.neighborhood}</div>
            <div className="col d-none d-md-inline">{listing.pets}</div>
            <div className="col ml-auto text-right">
                <div className="badge badge-pill badge-dark">${listing.price}</div><br/>
                {listing.no_fee_listing &&
                    <div className="badge badge-pill badge-info">no fee</div>
                }
            </div>

        </div>
    </div>
)


class PublicListings extends React.Component {
    constructor(props) {
        super(props)
        this.state = {
            filters: {},
            listings: [],
            total_listings: 0,
            more_listings_link: null,
            listing_detail: undefined,
            listing_marked: undefined,
            map_center: [-73.942423, 40.654089],
            map_zoom: [12],
            show_map: true,
            as_grid: true,
        }
    }
    hoverOn(listing) {
        if (listing)
            this.setState({
                map_center: coordinates(listing),
                listing_marked: listing
            })
        else
            this.setState({listing_marked: undefined})
    }
    hideDetail() {
        this.setState({
            listing_detail: undefined,
            listing_marked: undefined,
            map_zoom: [12]
        })
    }
    toggleOption(option) {
        this.setState({[option]: !this.state[option]})
    }
    fetchListings(params) {
        $.get(this.props.endpoint, params, (resp) =>
            this.setState({
                listings: resp.results,
                total_listings: resp.count,
                more_listings_link: resp.next
            })
        )
    }
    moreListings() {
        $.get(this.state.more_listings_link, (resp) =>
            this.setState({
                listings: this.state.listings.concat(resp.results),
                total_listings: resp.count,
                more_listings_link: resp.next
            })
        )
    }
    render() {
        const {constants} = this.props
        const {
            listings, total_listings, more_listings_link, listing_detail,
            filters, map_center, map_zoom, listing_marked, show_map, as_grid
        } = this.state

        const basic_filters = [
            "searching_text", "price", "beds", "baths", "nofeeonly", "amenities"
        ]
        const advanced_filters = [
            "hoods", "vacant", "pets_allowed", "price_per_bed", "listing_type",
            "address", "size", "owner_pays", "exclusive", "date_available"
        ]

        return <div>
            <Row key="mainrow1" style={{minHeight: 43}}>
                <FiltersBar filters={basic_filters}
                            advancedFilters={advanced_filters}
                            filtersState={filters}
                            constants={constants}
                            updateFilters={filters => this.setState({filters})}
                            updateParams={::this.fetchListings}
                />
                <Dropdown className="settings-dropdown">
                    <Dropdown.Toggle as={SettingsGear} />
                    <Dropdown.Menu alignRight>
                        <Dropdown.Item className="d-none d-md-block">
                            <Switch label="Toggle map" checked={show_map} onClick={() => this.toggleOption('show_map')}/>
                        </Dropdown.Item>
                        <Dropdown.Item>
                            <Switch label="Grid / List" checked={as_grid} onClick={() => this.toggleOption('as_grid')}/>
                        </Dropdown.Item>
                    </Dropdown.Menu>
                </Dropdown>
            </Row>
            <Row  key="mainrow2">
                <Col className="main-scroll left-main-column">
                        <center key="center"><h6>{total_listings} results</h6></center>
                        <Row key="row1" className="justify-content-center">
                            {listings.map(listing =>
                                as_grid ?
                                    <ListingGrid listing={listing}
                                                 key={listing.id}
                                                 hoverOn={::this.hoverOn} />
                                :
                                    <ListingList listing={listing}
                                                 key={listing.id}
                                                 hoverOn={::this.hoverOn} />
                            )}
                        </Row>
                        <Row key="row2" className="justify-content-center">
                            {more_listings_link ?
                                <Button variant="outline-primary" onClick={::this.moreListings} style={{padding: 5, margin: 10}}>
                                    Load more...
                                </Button>
                            :
                                <div style={{width: '100%', height: 12, borderBottom: '1px solid gray', textAlign: 'center'}}>
                                    <span style={{fontSize: '1em', backgroundColor: '#F3F5F6', padding: '0 10px'}}>
                                        End of results
                                    </span>
                                </div>
                            }
                        </Row>
                </Col>
                {show_map &&
                    <Col className={`map-panel ${listing_detail ? '' : 'd-none'} d-md-inline`}>
                        <MapComponent
                            listings={listings}
                            listing_highlighted={listing_marked || []}
                            center={map_center}
                            zoom={map_zoom}
                        />
                    </Col>
                }
            </Row>
        </div>
    }
}

ReactDOM.render(
    React.createElement(PublicListings, global.props),
    global.react_mount,
)
