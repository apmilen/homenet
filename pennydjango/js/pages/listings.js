import React from 'react'
import ReactDOM from 'react-dom'

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
            hover_address: null
        }
    }
    hoverOn(address) {
        this.setState({hover_address: address})
    }
    
    render() {
        const {listings} = this.props
        const edit_button = global.user && (global.user.is_staff || global.user.is_superuser)

        return (
            <div class="row main-content-row">
                <div class="col-md-6 main-scroll">
                    <div class="row">
                        {listings.map(listing =>
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
        )
    }
}

ReactDOM.render(
    React.createElement(Listings, global.props),
    global.react_mount,
)
