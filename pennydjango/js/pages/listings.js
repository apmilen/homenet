import React from 'react'
import ReactDOM from 'react-dom'

import {
    Row, Col, FormControl, InputGroup, ButtonToolbar, DropdownButton, Button
} from 'react-bootstrap'

import {tooltip} from '@/util/dom'


const FILTER_N_BEDS = [0, 1, 2, 3, 4]
const FILTER_MAX_N_BEDS = FILTER_N_BEDS.slice(-1)[0]

const FILTER_N_BATHS = [0, 1, 2, 3]
const FILTER_MAX_N_BATHS = FILTER_N_BATHS.slice(-1)[0]

const FILTER_PETS = ['Any', 'Allowed 😸', 'No Pets 😿']


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
        const edit_button = global.user && (global.user.is_staff || global.user.is_superuser)

        return (
            <div class="col-lg-6 col-md-12 p-1 card card-smallcard-post card-post--1 card-listing overlay-parent"
                 onMouseEnter={() => {hoverOn(listing.address)}}>
                <a className="overlay" href='#' onClick={() => {clickOn(listing.id)}}></a>
                <div class="card-post__image text-center">
                    <img class="box-wd" src={listing.default_image} />

                    {edit_button &&
                        <a class="card-post__category left-badge badge badge-pill badge-info"
                           href={listing.edit_link}>
                            <i class="material-icons">edit</i>
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
                                <td>Pets: {listing.pets_allowed ? 'Yes' : 'No'}</td>
                                <td>
                                    <i class="material-icons">place</i>Map
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
                        {listing.album.map((image_url, idx) =>
                            <li data-target="#carouselExampleIndicators" data-slide-to={idx}
                                class={idx == 0 ? 'active' : ''}></li>
                        )}
                    </ol>
                    <div class="carousel-inner">
                        {listing.album.map((image_url, idx) =>
                            <div class={`carousel-item ${idx == 0 ? 'active' : ''}`}>
                                <img class="d-block w-100" src={image_url} alt="First slide" />
                            </div>
                        )}
                    </div>
                    <a class="carousel-control-prev" href="#carouselExampleIndicators"
                       role="button" data-slide="prev">
                        <span class="carousel-control-prev-icon" aria-hidden="true"></span>
                        <span class="sr-only">Previous</span>
                    </a>
                    <a class="carousel-control-next" href="#carouselExampleIndicators"
                       role="button" data-slide="next">
                        <span class="carousel-control-next-icon" aria-hidden="true"></span>
                        <span class="sr-only">Next</span>
                    </a>
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
                            { listing.bedrooms } Beds
                        </div>
                        <div class="col-4 wrap-info p-0 pt-2 pb-2 border"
                             data-toggle="tooltip"
                             title={`${ listing.baths } Bath`}>
                            { listing.baths } Bath
                        </div>
                        <div class="col-4 p-0 pt-2 pb-2  border">
                            Pets: {listing.pets_allowed ? 'Yes' : 'No'}
                        </div>
                        <div class="col-8 wrap-info p-0 pt-2 pb-2 border"
                             data-toggle="tooltip"
                             title={ listing.address }>
                            { listing.address }
                        </div>
                        <div class="col-md-8 col-12 p-0 pt-2 pb-2 border">
                            <div class="col-12 text-justify border-bottom pt-2">
                                <p><b>About the place</b></p>
                                <p>{ listing.about }</p>
                            </div>
                            <div class="col-12 text-justify border-top pt-2">
                                <p><b>Amenities</b></p>
                                <ul class="ul-2">
                                    {listing.amenities.split(",").map(amenity =>
                                        <li>{ amenity }</li>
                                    )}
                                </ul>
                            </div>
                        </div>
                        <div class="col-md-4 col-12  p-0 pt-2 pb-2 border">
                            <p><b>Contact</b></p>
                            <p>{ listing.contact }</p>
                        </div>
                    </div>
                </div>
            </span>
        )
    }
}


class FiltersBar extends React.Component {
    filtering(e) {
        let {filters} = this.props
        filters[e.target.id] = e.target.value
        this.props.updateFilters(filters)
    }
    filterRooms(e) {
        let {filters} = this.props
        const num = parseInt(e.target.getAttribute('data-value'))
        const room_type = e.target.getAttribute('data-name')
        if (filters[room_type].has(num))
            filters[room_type].delete(num)
        else
            filters[room_type].add(num)
        this.props.updateFilters(filters)
    }
    switchPets(e) {
        let {filters} = this.props
        filters.pets_allowed = filters.pets_allowed + 1
        if(filters.pets_allowed >= FILTER_PETS.length)
            filters.pets_allowed = 0
        this.props.updateFilters(filters)
    }
    render() {
        const {filters} = this.props

        return (
            <ButtonToolbar style={{padding: 5}}>
                <div style={{width: '20vw', minWidth: 180}}>
                    <FormControl id='searching_text' size="sm"
                                 type='text'
                                 value={filters.searching_text}
                                 placeholder='Search for something you like :)'
                                 onChange={::this.filtering} />
                </div>
                &nbsp;
                <DropdownButton title='Price'>
                    <InputGroup style={{width: 300}}>
                        <InputGroup.Text>Min:</InputGroup.Text>
                        <FormControl id='price_min' xs='3' step='100'
                                     type='number' min='0' max={filters.price_max}
                                     value={filters.price_min}
                                     onChange={::this.filtering}
                                     placeholder='0'/>&nbsp;

                        <InputGroup.Text>Max:</InputGroup.Text>
                        <FormControl id='price_max' xs='3' step='100'
                                     type='number' min={filters.price_min}
                                     value={filters.price_max}
                                     onChange={::this.filtering}
                                     placeholder='9999'/>
                    </InputGroup>
                </DropdownButton>
                &nbsp;
                <DropdownButton title='Bedrooms'>
                    <div className='rooms-container'>
                        {FILTER_N_BEDS.map(n_beds =>
                            <div data-value={n_beds} data-name='beds'
                                 className={`room-div ${filters.beds.has(n_beds) ? 'selected' : ''}`}
                                 onClick={::this.filterRooms}>
                                {n_beds}{n_beds == FILTER_N_BEDS.slice(-1)[0] && '+'}
                            </div>
                        )}
                    </div>
                </DropdownButton>
                &nbsp;
                <DropdownButton title='Baths'>
                    <div className='rooms-container'>
                        {FILTER_N_BATHS.map(n_baths =>
                            <div data-value={n_baths} data-name='baths'
                                 className={`room-div ${filters.baths.has(n_baths) ? 'selected' : ''}`}
                                 onClick={::this.filterRooms}>
                                {n_baths}{n_baths == FILTER_N_BATHS.slice(-1)[0] && '+'}
                            </div>
                        )}
                    </div>
                </DropdownButton>
                &nbsp;
                <Button variant='primary'
                        onClick={::this.switchPets}>
                    Pets: {FILTER_PETS[filters.pets_allowed]}
                </Button>
            </ButtonToolbar>
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
                baths: new Set(FILTER_N_BATHS),
                pets_allowed: 0,
            },
            map_address: props.listings[0].address,
            show_detail: false,
        }
    }
    hoverOn(address) {
        this.setState({map_address: address})
    }
    showDetail(listing_id) {
        this.setState({
            show_detail: listing_id,
            map_address: this.props.listings.filter(listing => listing.id == listing_id)[0].address
        })
    }
    hideDetail() {
        this.setState({show_detail: false})
    }
    updateFilters(filters) {
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

        filtered_listings = filtered_listings.filter(
            listing => (
                filters.baths.has(listing.baths)
                || (filters.baths.has(FILTER_MAX_N_BATHS) && listing.baths >= FILTER_MAX_N_BATHS)
            )
        )

        if(filters.pets_allowed > 0){
            filtered_listings = filtered_listings.filter(
                listing => (
                    (filters.pets_allowed == 1 && listing.pets_allowed)
                    || (filters.pets_allowed == 2 && !listing.pets_allowed)
                )
            )
        }

        return filtered_listings
    }
    render() {
        const filtered_listings = this.filteredListings()

        return <span>
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
                        <Row className="justify-content-center">
                            <FiltersBar filters={this.state.filters} updateFilters={::this.updateFilters}/>
                        </Row>
                    </Col>
                }
            </Row>
            <Row>
                <Col md='6' className="main-scroll">
                    {this.state.show_detail ?
                        <Row>
                            <ListingDetail {...filtered_listings.filter(listing => listing.id == this.state.show_detail)[0]} />
                        </Row>
                    :
                        <span>
                        <center><h6>{filtered_listings.length} results</h6></center>
                        <Row>
                            {filtered_listings.map(listing =>
                                <ListingCard listing={listing}
                                             hoverOn={::this.hoverOn}
                                             clickOn={::this.showDetail}
                                        />
                            )}
                        </Row>
                        </span>
                    }
                </Col>
                <Col md='6' className={`map-panel ${this.state.show_detail ? '' : 'd-none'} d-md-inline`}>
                    <MapPanel address={this.state.map_address}/>
                </Col>
            </Row>
        </span>
    }
}

ReactDOM.render(
    React.createElement(Listings, global.props),
    global.react_mount,
)
