import React from 'react'

import {ButtonToolbar} from "shards-react";

import {
    searchingText, addressFilter, unitFilter, priceFilter, price_per_bedFilter,
    bedsFilter, bathsFilter, listing_typeFilter, listing_idFilter, sizeFilter,
    pets_allowedFilter, amenitiesFilter, nofeeonlyFilter, owner_paysFilter,
    exclusiveFilter, vacantFilter, draft_listingsFilter, date_availableFilter,
    sales_agentsFilter, listing_agentsFilter, hoodsFilter
} from "@/listings/filters"


export class ListingComponent extends React.Component {
    render() {
        const {
            full_address, no_fee_listing, detail, detail_link, default_image,
            price, price_per_bed, bedrooms, bathrooms, neighborhood, short_id,
            date_available, utilities, move_in_cost, size, landlord_contact,
            listing_agent, sales_agent, owner_pays, agent_notes, agent_bonus,
            pets, term, created, modified, status, listing_link, edit_link,
            offer_link
        } = this.props.listing

        return (
            <div className="row">
                <div className="col-12">
                    <div id="main-listing">
                        <div className="container-fluid new-listing-card">
                            <div className="row listing-admin-area">
                                <div className="col-12">
                                    <a href={listing_link} target="_blank"
                                       className="btn btn-sm btn-outline-info mr-1">{full_address}</a>
                                    <div className="dropdown" style={{display: 'inline-block'}}>
                                        <button
                                            className="btn btn-sm btn-outline-info mr-1 dropdown-toggle"
                                            type="button"
                                            id="dropdownManageButton"
                                            data-toggle="dropdown"
                                            aria-haspopup="true"
                                            aria-expanded="false">
                                            Manage
                                        </button>
                                        <div className="dropdown-menu dropdown-menu-small"
                                             aria-labelledby="dropdownManageButton">
                                            <a className="dropdown-item" href={edit_link}>
                                                <i className={'material-icons'}>edit</i> Edit
                                            </a>
                                            <a className="dropdown-item" href={detail_link}>
                                                <i className={'material-icons'}>format_list_bulleted</i> Details
                                            </a>
                                            <div className="dropdown-divider"></div>
                                            <a className="dropdown-item" href={offer_link}>
                                                <i className={'material-icons'}>create_new_folder</i> Create Offer
                                            </a>
                                        </div>
                                    </div>
                                    <button type="button"
                                            className="btn btn-sm btn-outline-info mr-1">Add
                                        to Listing Collection
                                    </button>
                                    {no_fee_listing && <span
                                        className="badge badge-info">No fee</span>}&nbsp;
                                    {detail.vacant && <span
                                        className="badge badge-info">Vacant</span>}
                                </div>
                            </div>
                            <div className="row listing-area-content">
                                <div className="col-lg-4 listing-area-main">
                                    <div className="row" style={{
                                        position: 'relative',
                                        paddingTop: '56.25%'
                                    }}>
                                        <a href={detail_link} target="_blank"
                                           rel="noreferrer noopener">
                                            <img className="lazy img-fluid mx-auto"
                                                 src={default_image}
                                                 width="960"
                                                 height="540"
                                                 style={{
                                                     position: 'absolute',
                                                     top: 0,
                                                     left: 0,
                                                     width: '100%',
                                                     height: '100%'
                                                 }}/>
                                        </a>
                                    </div>
                                    <div className="row">
                                        <div
                                            className="listing-card-stub container-fluid">
                                            <div className="row">
                                                <div className="col-6">
                                                    <span>${price}</span>
                                                </div>
                                                <div className="col-6">
                                                    <span>${price_per_bed}/bed</span>
                                                </div>
                                            </div>
                                            <div className="row">
                                                <div className="col-6">
                                                    <i className="fa fa-bed"></i> {bedrooms} Bed
                                                </div>
                                                <div className="col-6">
                                                    <i className="fa fa-bath"></i> {bathrooms} Bath
                                                </div>
                                            </div>
                                            <div className="row">
                                                <div className="col-12">
                                                    <i className="material-icons">place</i>
                                                    <a href={detail_link}>
                                                        {full_address}
                                                    </a>
                                                </div>
                                            </div>
                                            <div className="row">
                                                <div className="col-12">
                                                    {neighborhood}
                                                </div>
                                            </div>
                                            <div className="row">
                                                <div className="col-12">Subways
                                                </div>
                                            </div>
                                            <div className="row">
                                                <div
                                                    className="col-12 border-bottom-0">Streets
                                                </div>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                                <div className="col-lg-4 listing-first-data-col">
                                    <div className="row listing-area-data-row">
                                        <div className="col-sm-4 text-left">
                                            <b>ID</b></div>
                                        <div
                                            className="col-sm-8 text-left">{short_id}</div>
                                    </div>
                                    <div className="row listing-area-data-row">
                                        <div className="col-sm-4 text-left"><b>Date
                                            Available</b></div>
                                        <div
                                            className="col-sm-8 text-left">{date_available}</div>
                                    </div>
                                    <div className="row listing-area-data-row">
                                        <div className="col-sm-4 text-left">
                                            <b>Access</b></div>
                                        <div
                                            className="col-sm-8 text-left">{detail.building_access}</div>
                                    </div>
                                    <div className="row listing-area-data-row">
                                        <div className="col-sm-4 text-left">
                                            <b>Utilities</b></div>
                                        <div
                                            className="col-sm-8 text-left">{utilities}</div>
                                    </div>
                                    <div className="row listing-area-data-row">
                                        <div className="col-sm-4 text-left"><b>Move
                                            in Cost</b></div>
                                        <div
                                            className="col-sm-8 text-left">{move_in_cost}</div>
                                    </div>
                                    <div className="row listing-area-data-row">
                                        <div className="col-sm-4 text-left"><b>Square
                                            Feet</b></div>
                                        <div className="col-sm-8">{size}</div>
                                    </div>
                                    <div className="row listing-area-data-row">
                                        <div className="col-sm-4"><b>Landlord</b>
                                        </div>
                                        <div
                                            className="col-sm-8">{detail.landlord_contact}</div>
                                    </div>
                                    <div className="row text-center">
                                        <div className="col-6">
                                            <h6>Listing</h6>
                                            <a className="contact-avatar"
                                               href={listing_agent.profile_link}
                                               target="_blank">
                                                <div className="circle-avatar"
                                                     style={{backgroundImage: `url(${listing_agent.avatar_url})`}}></div>
                                            </a>
                                            {listing_agent.first_name} {listing_agent.last_name}
                                        </div>
                                        <div className="col-6">
                                            <h6>Sales</h6>
                                            <a className="contact-avatar"
                                               href={sales_agent.profile_link}
                                               target="_blank">
                                                <div className="circle-avatar"
                                                     style={{backgroundImage: `url(${sales_agent.avatar_url})`}}></div>
                                            </a>
                                            {sales_agent.first_name} {sales_agent.last_name}
                                        </div>
                                        <hr/>
                                    </div>
                                </div>
                                <div className="col-lg-4 listing-second-data-col">
                                    <div className="row listing-area-data-row">
                                        <div className="col-sm-4 text-left"><b>Owner
                                            Pays</b></div>
                                        <div
                                            className="col-sm-8 text-left">{owner_pays}%
                                        </div>
                                    </div>
                                    <div className="row listing-area-data-row">
                                        <div className="col-sm-4 text-left"><b>Agent
                                            Notes</b></div>
                                        <div
                                            className="col-sm-8 text-left">{agent_notes}</div>
                                    </div>
                                    <div className="row listing-area-data-row">
                                        <div className="col-sm-4 text-left"><b>Agent
                                            Bonus</b></div>
                                        <div
                                            className="col-sm-8 text-left">{agent_bonus}</div>
                                    </div>
                                    <div className="row listing-area-data-row">
                                        <div className="col-sm-4 text-left">
                                            <b>Pets</b></div>
                                        <div
                                            className="col-sm-8 text-left">{pets}</div>
                                    </div>
                                    <div className="row listing-area-data-row">
                                        <div className="col-sm-4 text-left">
                                            <b>Term</b></div>
                                        <div
                                            className="col-sm-8 text-left">{term}</div>
                                    </div>
                                    <div className="row listing-area-data-row">
                                        <div className="col-sm-4 text-left">
                                            <b>Created</b></div>
                                        <div
                                            className="col-sm-8 text-left">{created}</div>
                                    </div>
                                    <div className="row listing-area-data-row">
                                        <div className="col-sm-4 text-left">
                                            <b>Updated</b></div>
                                        <div
                                            className="col-sm-8 text-left">{modified}</div>
                                    </div>
                                    <div className="row listing-area-data-row">
                                        <div className="col-sm-4 text-left">
                                            <b>Share</b></div>
                                        <div className="col-sm-8 text-left">
                                            <button
                                                className="btn btn-pill btn-outline-info">
                                                Copy to Clipboard
                                            </button>
                                        </div>
                                    </div>
                                    <div
                                        className="row listing-area-data-row border-bottom-0">
                                        <div className="col-sm-4 text-left">
                                            <b>Status</b></div>
                                        <div
                                            className="col-sm-8 text-left">{status}</div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        )
    }
}


export class FiltersBar extends React.Component {
    constructor(props) {
        super(props)
        this.state = props.filters
    }

    filtering(e) {
        this.setState({[e.target.id]: e.target.value}, this.fetchListings)
    }

    filterMultipleSelection(e) {
        const value = e.target.id
        const item_type = e.target.getAttribute('name')
        const current_filter = this.state[item_type]

        const new_filter = current_filter.includes(value) ?
            current_filter.filter(val => val != value) :
            current_filter.concat(value)

        this.setState({[item_type]: new_filter}, this.fetchListings)
    }

    filterOneSelection(e) {
        const f_name = e.target.getAttribute('name')
        const f_value = e.target.getAttribute('value')
        this.setState({[f_name]: f_value}, this.fetchListings)
    }

    filterToggle(e) {
        const f_name = e.target.getAttribute('name')
        this.setState({[f_name]: !this.state[f_name]}, this.fetchListings)
    }

    filterRange(e) {
        const f_name = e.target.getAttribute('name')
        const range = [$('#' + f_name + '_min').val(), $('#' + f_name + '_max').val()]
        this.setState({[f_name]: range}, this.fetchListings)
    }

    changeDate(date) {
        this.setState({date_available: date || ''}, this.fetchListings)
    }

    fetchListings() {
        this.props.updateParentState({filters: this.state})
        $.get(this.props.endpoint, this.state, (resp) =>
            this.props.updateParentState({listings: resp.results})
        )
    }

    voidFunc(e) {
        console.log("not implemented", e.target)
    }

    componentDidMount() {
        this.fetchListings()
    }

    render() {
        const {
            searching_text, address, unit, price, price_per_bed, beds, baths,
            listing_type, listing_id, size, pets_allowed, amenities, nofeeonly,
            owner_pays, exclusive, vacant, draft_listings, date_available,

            sales_agents, listing_agents, hoods
        } = this.state

        return (
            <ButtonToolbar style={{padding: 5}}>

                {searching_text != undefined &&
                [searchingText(searching_text, ::this.filtering), '\u00A0']}

                {address != undefined &&
                [addressFilter(address, ::this.filtering), '\u00A0']}

                {unit != undefined &&
                [unitFilter(unit, ::this.filtering), '\u00A0']}

                {price != undefined &&
                [priceFilter(price, ::this.filterRange), '\u00A0']}

                {price_per_bed != undefined &&
                [price_per_bedFilter(price_per_bed, ::this.filterRange), '\u00A0']}

                {beds != undefined &&
                [bedsFilter(beds, ::this.filterMultipleSelection), '\u00A0']}

                {baths != undefined &&
                [bathsFilter(baths, ::this.filterMultipleSelection), '\u00A0']}

                {listing_type != undefined &&
                [listing_typeFilter(listing_type, this.props.constants.listing_types, ::this.filterOneSelection), '\u00A0']}

                {listing_id != undefined &&
                [listing_idFilter(listing_id, ::this.filtering), '\u00A0']}

                {size != undefined &&
                [sizeFilter(size, ::this.filterRange), '\u00A0']}

                {pets_allowed != undefined &&
                [pets_allowedFilter(pets_allowed, this.props.constants.pets_allowed, ::this.filterOneSelection), '\u00A0']}

                {amenities != undefined &&
                [amenitiesFilter(amenities, this.props.constants.amenities, ::this.filterMultipleSelection), '\u00A0']}

                {nofeeonly != undefined &&
                [nofeeonlyFilter(nofeeonly, ::this.filterToggle), '\u00A0']}

                {owner_pays != undefined &&
                [owner_paysFilter(owner_pays, ::this.filterToggle), '\u00A0']}

                {exclusive != undefined &&
                [exclusiveFilter(exclusive, ::this.filterToggle), '\u00A0']}

                {vacant != undefined &&
                [vacantFilter(vacant, ::this.filterToggle), '\u00A0']}

                {draft_listings != undefined &&
                [draft_listingsFilter(draft_listings, ::this.filterToggle), '\u00A0']}

                {date_available != undefined &&
                [date_availableFilter(date_available, ::this.changeDate), '\u00A0']}

                {/* BELOW NOT IMPLEMENTED YET */}
                {sales_agents != undefined &&
                [sales_agentsFilter(sales_agents, ::this.voidFunc), '\u00A0']}

                {listing_agents != undefined &&
                [listing_agentsFilter(listing_agents, ::this.voidFunc), '\u00A0']}

                {hoods != undefined &&
                [hoodsFilter(hoods, ::this.voidFunc), '\u00A0']}

            </ButtonToolbar>
        )
    }
}

