import React from 'react'
import ReactDOM from 'react-dom'

import {
    FormControl, Row, InputGroup, Container, ButtonToolbar, DropdownButton
} from 'react-bootstrap'

import {tooltip} from '@/util/dom'


const FILTER_N_BEDS = [1, 2, 3, 4]
const FILTER_MAX_N_BEDS = FILTER_N_BEDS.slice(-1)[0]


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
                beds: new Set(FILTER_N_BEDS),
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
    filterBeds(e) {
        let {filters} = this.state
        const num = parseInt(e.target.getAttribute('data-value'))
        if (filters.beds.has(num))
            filters.beds.delete(num)
        else
            filters.beds.add(num)
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

        filtered_listings = filtered_listings.filter(
            listing => (
                filters.beds.has(listing.bedrooms)
                || (filters.beds.has(FILTER_MAX_N_BEDS) && listing.bedrooms >= FILTER_MAX_N_BEDS)
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

                        <ButtonToolbar>
                            <div style={{width: '20vh'}}>
                                <FormControl id='searching_text' size="sm"
                                             type='text'
                                             value={filters.searching_text}
                                             placeholder='Search for something you like :)'
                                             onChange={::this.filtering} />
                            </div>&nbsp;
                            <DropdownButton title='Price'>
                                <Container style={{width: 300}}>
                                    <InputGroup>
                                        <InputGroup.Text>Min:</InputGroup.Text>
                                        <FormControl id='price_min' xs='3' step='100'
                                                     type='number' min='0'
                                                     value={filters.price_min}
                                                     onChange={::this.filtering}
                                                     placeholder='0'/>&nbsp;

                                        <InputGroup.Text>Max:</InputGroup.Text>
                                        <FormControl id='price_max' xs='3' step='100'
                                                     type='number' min='0'
                                                     value={filters.price_max}
                                                     onChange={::this.filtering}
                                                     placeholder='9999'/>
                                    </InputGroup>
                                </Container>
                            </DropdownButton>
                            &nbsp;
                            <DropdownButton title='Bedrooms'>
                                <div className='beds-container'>
                                    {FILTER_N_BEDS.map(n_beds =>
                                        <div data-value={n_beds}
                                             className={`bed-div ${filters.beds.has(n_beds) ? 'selected' : ''}`}
                                             onClick={::this.filterBeds}>
                                            {n_beds}{n_beds == FILTER_N_BEDS.slice(-1)[0] && '+'}
                                        </div>
                                    )}
                                </div>
                            </DropdownButton>
                        </ButtonToolbar>
                    </Row>
            </Container>
            <div class="row">
                <div class="col-md-6 main-scroll">
                    <center><h6>{filtered_listings.length} results</h6></center>
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
