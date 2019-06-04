import React from 'react'
import ReactDOM from 'react-dom'

import {Row, Col} from "shards-react";

import {tooltip} from '@/util/dom'
import {FiltersBar} from '@/listings/components'



class MapPanel extends React.Component {
    render() {
        return (
            <iframe src={`https://maps.google.com/maps?q=${this.props.address}&t=&z=13&ie=UTF8&iwloc=&output=embed`}
                frameborder="0" width="100%" height="100%" scrolling="no"
                marginheight="0" marginwidth="0"
                style={{display: 'inline-block'}}></iframe>
        )
    }
}


class ListingCard extends React.Component {
    render() {
        const {listing, hoverOn, clickOn} = this.props

        return (
            <div class="col-lg-6 col-md-12 p-1 card card-smallcard-post card-post--1 card-listing overlay-parent"
                 onMouseEnter={() => {hoverOn(listing.address)}}>
                <a className="overlay" href='#' onClick={() => {clickOn(listing.id)}}></a>
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
                                <td>{listing.pets}</td>
                                <td>
                                    <i className="material-icons">share</i> Share
                                </td>
                                <td>
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
            map_address: '',
            show_detail: false,
        }
    }
    hoverOn(address) {
        this.setState({map_address: address})
    }
    showDetail(listing_id) {
        this.setState({
            show_detail: listing_id,
            map_address: this.state.listings.find(listing => listing.id == listing_id).address
        })
    }
    hideDetail() {
        this.setState({show_detail: false})
    }
    render() {
        const {listings} = this.state

        return [
            <Row style={{minHeight: 43}}>
                {this.state.show_detail ?
                    <a href='#'
                       style={{margin: 'auto 0 auto 35px'}}
                       onClick={::this.hideDetail}>
                        <i class="material-icons">keyboard_arrow_left</i>
                        Back to results
                    </a>
                :
                    <Col>
                        <Row className="justify-content-center home-filters">
                            <FiltersBar filters={this.state.filters}
                                        constants={this.props.constants}
                                        endpoint={this.props.endpoint}
                                        updateParentState={new_state => this.setState(new_state)} />
                        </Row>
                    </Col>
                }
            </Row>,
            <Row>
                <Col md='6' className="main-scroll">
                    {this.state.show_detail ?
                        <Row>
                            <ListingDetail {...listings.find(listing => listing.id == this.state.show_detail)} />
                        </Row>
                    : [
                        <center><h6>{listings.length} results</h6></center>,
                        <Row>
                            {listings.map(listing =>
                                <ListingCard listing={listing}
                                             hoverOn={::this.hoverOn}
                                             clickOn={::this.showDetail} />
                            )}
                        </Row>
                    ]}
                </Col>
                <Col md='6' className={`map-panel ${this.state.show_detail ? '' : 'd-none'} d-md-inline`}>
                    <MapPanel address={this.state.map_address}/>
                </Col>
            </Row>
        ]
    }
}

ReactDOM.render(
    React.createElement(PublicListings, global.props),
    global.react_mount,
)
