import React from 'react'
import ReactDOM from 'react-dom'

import FormControl from 'react-bootstrap/FormControl'
import Button from 'react-bootstrap/Button'
import Row from 'react-bootstrap/Row'
import Col from 'react-bootstrap/Col'
import InputGroup from 'react-bootstrap/InputGroup'
import Popover from 'react-bootstrap/Popover'
import OverlayTrigger from 'react-bootstrap/OverlayTrigger'
import Container from 'react-bootstrap/Container'

import {tooltip} from '@/util/dom'


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


class Listings extends React.Component {
    constructor(props) {
        super(props)
        this.state = {
            filters: {
                searching_text: '',
                price_min: '',
                price_max: '',
            },
            hover_address: props.listings[0].address
        }
    }
    hoverOn(address) {
        this.setState({hover_address: address})
    }
    filtering(e) {
        let {filters} = this.state
        filters[e.target.id] = e.target.value
        this.setState(filters)
    }
    filteredListings() {
        const {listings} = this.props
        let filtered_listings = listings

        const {filters} = this.state
        const query = filters.searching_text.toLowerCase()

        filtered_listings = filtered_listings.filter(
            listing => (
                listing.address.toLowerCase().includes(query)
                || listing.about.toLowerCase().includes(query)
                || listing.amenities.toLowerCase().includes(query)
            )
        )

        filtered_listings = filtered_listings.filter(
            listing => (
                listing.price >= (filters.price_min || 0)
                && listing.price <= (filters.price_max || Infinity)
            )
        )

        return filtered_listings
    }
    render() {
        const filtered_listings = this.filteredListings()
        const {filters} = this.state
        const edit_button = global.user && (global.user.is_staff || global.user.is_superuser)

        return <div class="content-wrapper">
            <Container className='filters-bar'>
                    <Row className="justify-content-md-center">
                        <Col xs='7' md='5' lg='3'>
                            <FormControl id='searching_text' size="sm"
                                         type='text'
                                         value={filters.searching_text}
                                         placeholder='Search for something you like :)'
                                         onChange={::this.filtering} />
                        </Col>
                        <Col xs='5' md='4' lg='3'>
                            <OverlayTrigger trigger="click"
                                            placement='bottom'
                                            overlay={
                                <Popover title='Type range'>
                                    <Row>
                                        <InputGroup>
                                            <InputGroup.Text>Min:</InputGroup.Text>
                                            <FormControl id='price_min' xs='3'
                                                         type='number' min='0'
                                                         value={filters.price_min}
                                                         onChange={::this.filtering}
                                                         placeholder='0'/>&nbsp;

                                            <InputGroup.Text>Max:</InputGroup.Text>
                                            <FormControl id='price_max' xs='3'
                                                         type='number' min='0'
                                                         value={filters.price_max}
                                                         onChange={::this.filtering}
                                                         placeholder='9999'/>
                                        </InputGroup>
                                    </Row>
                                </Popover>
                            }>
                                <Button variant="outline-secondary" size="sm">
                                    Price {filters.price_min} {filters.price_max}
                                </Button>
                            </OverlayTrigger>
                        </Col>
                    </Row>
            </Container>
            <div class="row">
                <div class="col-md-6 main-scroll">
                    <div class="row">
                        {filtered_listings.map(listing =>
                            <div class="col-lg-6 col-md-12 p-1 card card-smallcard-post card-post--1 card-listing"
                                 onMouseEnter={() => {this.hoverOn(listing.address)}}>
                                <div class="card-post__image text-center">
                                    <img class="box-wd" src={listing.default_image} />

                                    {edit_button &&
                                        <a class="card-post__category left-badge badge badge-pill badge-info"
                                           href={listing.edit_link}>
                                            <i  class="material-icons">edit</i>
                                            Edit
                                        </a>
                                    }
                                  
                                    <span class="card-post__category badge badge-pill badge-dark">${listing.price}</span>
                                </div>
                                <div class="card-body p-0 text-center">
                                    <table class="table mb-0 listing-info">
                                        <tbody>
                                            <tr>
                                                <td class="wrap-info"
                                                    {...tooltip(`${listing.bedrooms} Beds / ${listing.baths} Bath`)}>
                                                    {listing.bedrooms} Beds / {listing.baths} Bath
                                                </td>
                                                <td class="wrap-info" colspan="2"
                                                    {...tooltip(listing.address)}>
                                                    {listing.address}
                                                </td>
                                            </tr>
                                            <tr>
                                                <td>Pets: {listing.pets_allowed}</td>
                                                <td>
                                                    <a href={listing.detail_link}>
                                                        <i class="material-icons">home</i>
                                                        Detail
                                                    </a>
                                                </td>
                                            </tr>
                                        </tbody>
                                    </table>
                                </div>
                            </div>
                        )}
                    </div>
                </div>
                <div class="col-md-6 p-0 map-panel">
                    <MapPanel address={this.state.hover_address}/>
                </div>
            </div>
        </div>
    }
}

ReactDOM.render(
    React.createElement(Listings, global.props),
    global.react_mount,
)
