import React from 'react'
import ReactDOM from 'react-dom'

import {Row, Col, Button} from "shards-react";

import {tooltip} from '@/util/dom'
import {FiltersBar} from '@/listings/components'

import {MapComponent, coordinates} from '@/components/maps'


class ListingCard extends React.Component {
    render() {
        const {listing, hoverOn, clickOn} = this.props

        return (
            <div class="col-lg-6 col-md-12 px-1 card card-smallcard-post card-post--1 card-listing overlay-parent"
                 onMouseEnter={() => {hoverOn(listing)}} onMouseLeave={() => {hoverOn(undefined)}}>
                <a className="overlay" href='#' onClick={() => {clickOn(listing)}}></a>
                <div class="card-post__image text-center">
                    <img class="box-wd" src={listing.default_image} />
                    {listing.no_fee_listing &&
                        <span class="card-post__category left-badge badge badge-pill badge-info">no fee</span>
                    }
                    <span class="card-post__category badge badge-pill badge-dark">${listing.price}</span>
                </div>
                <div class="card-body p-0 text-center">
                    <table class="table mb-0 listing-info">
                        <tbody>
                            <tr>
                                <td class="wrap-info"
                                    {...tooltip(`${listing.bedrooms} Beds / ${listing.baths} Bath`)}>
                                    {parseFloat(listing.bedrooms).toString()} Beds / {parseFloat(listing.bathrooms).toString()} Bath
                                </td>
                                <td class="wrap-info" colspan="2"
                                    {...tooltip(listing.address)}>
                                    {listing.neighborhood}
                                </td>
                            </tr>
                            <tr>
                                <td class="wrap-info">{listing.pets}</td>
                                <td class="wrap-info">
                                    <i className="material-icons">share</i> Share
                                </td>
                                <td class="wrap-info">
                                    <i className="material-icons">place</i>Map
                                </td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </div>
        )
    }
}


class ListingDetail extends React.Component {
    render(){
        const listing = this.props

        return (
            <span>
                <div id="carouselExampleIndicators" class="carousel slide"
                     data-ride="carousel" data-interval="2500">
                    <ol class="carousel-indicators">
                        {listing.images.map((image_url, idx) =>
                            <li data-target="#carouselExampleIndicators" data-slide-to={idx}
                                class={idx == 0 ? 'active' : ''}></li>
                        )}
                    </ol>
                    <div class="carousel-inner">
                        {listing.images.map((image_url, idx) =>
                            <div class={`carousel-item ${idx == 0 ? 'active' : ''}`}>
                                <img class="d-block w-100" src={image_url} alt="First slide" />
                            </div>
                        )}
                    </div>
                    {listing.images.length > 1 ? [
                        <a class="carousel-control-prev" href="#carouselExampleIndicators"
                           role="button" data-slide="prev">
                            <span class="carousel-control-prev-icon" aria-hidden="true"></span>
                            <span class="sr-only">Previous</span>
                        </a>,
                        <a class="carousel-control-next" href="#carouselExampleIndicators"
                           role="button" data-slide="next">
                            <span class="carousel-control-next-icon" aria-hidden="true"></span>
                            <span class="sr-only">Next</span>
                        </a>] : null}
                </div>

                <div class="card card-smallcard-post card-post--1 card-listing">
                    <div class="card-body p-0 text-center row m-0">
                        <div class="col-4 wrap-info p-0 pt-2 pb-2 border border"
                             data-toggle="tooltip"
                             title={`$${ listing.price }/Month`}>
                            ${ listing.price }/Month
                        </div>
                        <div class="col-4 wrap-info p-0 pt-2 pb-2 border"
                             data-toggle="tooltip"
                             title={`${ listing.bedrooms } Beds`}>
                            { parseFloat(listing.bedrooms).toString() } Beds
                        </div>
                        <div class="col-4 wrap-info p-0 pt-2 pb-2 border"
                             data-toggle="tooltip"
                             title={`${ listing.baths } Bath`}>
                            { parseFloat(listing.bathrooms).toString() } Bath
                        </div>
                        <div class="col-4 p-0 pt-2 pb-2  border">
                            Pets: { listing.pets }
                        </div>
                        <div class="col-8 wrap-info p-0 pt-2 pb-2 border"
                             data-toggle="tooltip"
                             title={ listing.address }>
                            { listing.address }
                        </div>
                        <div class="col-md-8 col-12 p-0 pt-2 pb-2 border">
                            <div class="col-12 text-justify border-bottom pt-2">
                                <p><b>About the place</b></p>
                                <p>{ listing.description }</p>
                            </div>
                            <div class="col-12 text-justify border-top pt-2">
                                <p><b>Amenities</b></p>
                                <ul class="ul-2">
                                    {listing.amenities.map(amenity =>
                                        <li>{ amenity }</li>
                                    )}
                                </ul>
                            </div>
                        </div>
                        <div class="col-md-4 col-12  p-0 pt-2 pb-2 border ">
                            <p><b>Contact</b></p>
                            <a class="contact-avatar" href="#" role="button">
                                <div class="circle-avatar" style={{ backgroundImage: `url(${ listing.sales_agent.avatar_url })`}}></div>
                            </a>
                            <div>{ listing.sales_agent.first_name }</div>
                        </div>
                    </div>
                </div>
            </span>
        )
    }
}


class PublicListings extends React.Component {
    constructor(props) {
        super(props)
        this.state = {
            filters: {
                searching_text: '',
                price: [],
                beds: [],
                baths: [],
                pets_allowed: 'any',
                nofeeonly: false,
                amenities: [],
            },
            listings: [],
            total_listings: 0,
            more_listings_link: null,
            listing_detail: undefined,
            map_center: [-73.942423, 40.654089],
        }
    }
    hoverOn(listing) {
        if (listing)
            this.setState({map_center: coordinates(listing)})
    }
    showDetail(listing) {
        this.setState({listing_detail: listing})
    }
    hideDetail() {
        this.setState({listing_detail: undefined})
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
        const {constants, endpoint} = this.props
        const {
            listings, total_listings, more_listings_link,
            listing_detail, filters, map_center
        } = this.state

        return [
            <Row style={{minHeight: 43}}>
                {listing_detail ?
                    <a href='#'
                       style={{margin: 'auto 0 auto 35px'}}
                       onClick={::this.hideDetail}>
                        <i class="material-icons">keyboard_arrow_left</i>
                        Back to results
                    </a>
                :
                    <Col>
                        <Row className="justify-content-center home-filters">
                            <FiltersBar filters={filters} constants={constants} endpoint={endpoint}
                                        updateParentState={new_state => this.setState(new_state)} />
                        </Row>
                    </Col>
                }
            </Row>,
            <Row>
                <Col md='6' className="main-scroll">
                    {listing_detail ?
                        <Row>
                            <ListingDetail {...listing_detail} />
                        </Row>
                    : [
                        <center><h6>{total_listings} results</h6></center>,
                        <Row>
                            {listings.map(listing =>
                                <ListingCard listing={listing}
                                             hoverOn={::this.hoverOn}
                                             clickOn={::this.showDetail} />
                            )}
                        </Row>,
                        <Row className="justify-content-center">
                            {more_listings_link ?
                                <Button outline onClick={::this.moreListings} style={{padding: 5, margin: 10}}>
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
                    ]}
                </Col>
                <Col md='6' className={`map-panel ${listing_detail ? '' : 'd-none'} d-md-inline`}>
                    <MapComponent
                        listings={listings}
                        center={map_center}
                        clickOn={::this.showDetail}
                    />
                </Col>
            </Row>
        ]
    }
}

ReactDOM.render(
    React.createElement(PublicListings, global.props),
    global.react_mount,
)
