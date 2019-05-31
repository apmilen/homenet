import React from 'react'

import {FormControl, DropdownButton} from 'react-bootstrap'
import {
    Button, ButtonToolbar, InputGroup, InputGroupText, FormRadio, FormCheckbox
} from "shards-react";



const searchingText = (searching_text, func) =>
    <div style={{width: '20vw', minWidth: 180}}>
        <FormControl id='searching_text' size="sm"
                     type='text'
                     value={searching_text}
                     placeholder='Search for something you like :)'
                     onChange={func} />
    </div>

const priceFilter = (price_min, price_max, func) =>
    <DropdownButton title='Price'>
        <InputGroup style={{width: 300}}>
            <InputGroupText>Min:</InputGroupText>
            <FormControl id='price_min' xs='3' step='100'
                         type='number' min='0' max={price_max}
                         value={price_min}
                         onChange={func}
                         placeholder='0'/>&nbsp;

            <InputGroupText>Max:</InputGroupText>
            <FormControl id='price_max' xs='3' step='100'
                         type='number' min={price_min}
                         value={price_max}
                         onChange={func}
                         placeholder='9999'/>
        </InputGroup>
    </DropdownButton>

const bedsFilter = (beds, func) =>
    <DropdownButton title='Bedrooms'>
        <div className='rooms-container'>
            {["0", "1", "2", "3", "4+"].map(n_beds =>
                <div id={n_beds} name='beds'
                     className={`room-div ${beds.includes(n_beds) ? 'selected' : ''}`}
                     onClick={func}>
                    {n_beds}
                </div>
            )}
        </div>
    </DropdownButton>

const bathsFilter = (baths, func) =>
    <DropdownButton title='Baths'>
        <div className='rooms-container'>
            {["0", "1", "2", "3+"].map(n_baths =>
                <div id={n_baths} name='baths'
                     className={`room-div ${baths.includes(n_baths) ? 'selected' : ''}`}
                     onClick={func}>
                    {n_baths}
                </div>
            )}
        </div>
    </DropdownButton>

const pets_allowedFilter = (pets_allowed, pets_allowed_dict, func) =>
    <DropdownButton title='Pets'>
        <div className='pets-container'>
            <FormRadio
                name='any'
                checked={pets_allowed == 'any'}
                onChange={func} >
            Any
            </FormRadio>
            {Object.keys(pets_allowed_dict).map(allowed_type =>
                <FormRadio
                    name={allowed_type}
                    checked={pets_allowed == allowed_type}
                    onChange={func} >
                {pets_allowed_dict[allowed_type]}
                </FormRadio>
            )}
        </div>
    </DropdownButton>

const amenitiesFilter = (amenities, amenities_dict, func) =>
    <DropdownButton title='Amenities'>
        <div className='amenities-container'>
            {Object.keys(amenities_dict).map(amenity =>
                <FormCheckbox id={amenity} name="amenities"
                              checked={amenities.includes(amenity)}
                              onChange={func}>
                    {amenities_dict[amenity]}
                </FormCheckbox>
            )}
        </div>
    </DropdownButton>

const nofeeonlyFilter = (nofeeonly, func) =>
    <Button outline={!nofeeonly} onClick={func} name="nofeeonly">
        No Fee Only
    </Button>

const draft_listingsFilter = (draft_listings, func) =>
    <Button outline={!draft_listings} onClick={func} name="draft_listings">
        Draft Listings
    </Button>

const addressFilter = (address, func) =>
    <div style={{width: '14vw', minWidth: 100}}>
        <FormControl id='address' size="sm"
                     type='text'
                     value={address}
                     placeholder='Address'
                     onChange={func} />
    </div>

const unitFilter = (unit, func) =>
    <div style={{width: '6vw', minWidth: 50}}>
        <FormControl id='unit' size="sm"
                     type='text'
                     value={unit}
                     placeholder='Unit'
                     onChange={func} />
    </div>

const owner_paysFilter = (owner_pays, func) =>
    <Button outline={!owner_pays} onClick={func} name="owner_pays">
        Owner Pays
    </Button>

const exclusiveFilter = (exclusive, func) =>
    <Button outline={!exclusive} onClick={func} name="exclusive">
        Exclusive
    </Button>

const vacantFilter = (vacant, func) =>
    <Button outline={!vacant} onClick={func} name="vacant">
        Vacant
    </Button>



const sales_agentsFilter = (sales_agent, func) =>
    <div></div>

const listing_agentsFilter = (listing_agent, func) =>
    <div></div>

const hoodsFilter = (hoods, func) =>
    <div></div>

const price_per_bedFilter = (price_per_bed, func) =>
    <div></div>

const listing_typeFilter = (listing_type, func) =>
    <div></div>

const listing_idFilter = (listing_id, func) =>
    <div></div>

const sizeFilter = (size, func) =>
    <div></div>

const statusFilter = (status, func) =>
    <div></div>

const date_availableFilter = (date_available, func) =>
    <div></div>





export class FiltersBar extends React.Component {
    constructor(props) {
        super(props)
        this.state = props.filters
    }
    filtering(e) {
        this.setState({ [e.target.id]: e.target.value }, this.filterListings)
    }
    updateFilter(e) {
        const value = e.target.id
        const item_type = e.target.getAttribute('name')
        const current_filter = this.state[item_type]

        const new_filter = current_filter.includes(value) ?
                           current_filter.filter(val => val != value) :
                           current_filter.concat(value)

        this.setState({[item_type]: new_filter}, this.filterListings)
    }
    changePets(e) {
        this.setState({ pets_allowed: e.target.name }, this.filterListings)
    }
    toggleFilter(e) {
        const f_name = e.target.getAttribute('name')
        this.setState({ [f_name]: !this.state[f_name] }, this.filterListings)
    }
    filterListings() {
        this.props.updateParentState({filters: this.state})
        $.get(this.props.endpoint, this.state, (resp) =>
            this.props.updateParentState({listings: resp.results})
        )
    }
    voidFunc(e) {
        console.log("not implemented", e.target)
    }
    componentDidMount() {
        this.filterListings()
    }
    render() {
        const {
            searching_text, address, unit, price_min, price_max, beds, baths,
            pets_allowed, amenities, nofeeonly, owner_pays, exclusive, vacant,
            draft_listings,

            sales_agents, listing_agents, hoods, price_per_bed,
            listing_type, listing_id, size, status, date_available
        } = this.state

        return (
            <ButtonToolbar style={{padding: 5}}>

                {searching_text != undefined &&
                    [searchingText(searching_text, ::this.filtering), '\u00A0']}

                {address != undefined &&
                    [addressFilter(address, ::this.filtering), '\u00A0']}

                {unit != undefined &&
                    [unitFilter(unit, ::this.filtering), '\u00A0']}

                {(price_min != undefined && price_max != undefined) &&
                    [priceFilter(price_min, price_max, ::this.filtering), '\u00A0']}

                {beds != undefined &&
                    [bedsFilter(beds, ::this.updateFilter), '\u00A0']}

                {baths != undefined &&
                    [bathsFilter(baths, ::this.updateFilter), '\u00A0']}

                {pets_allowed != undefined &&
                    [pets_allowedFilter(pets_allowed, this.props.constants.pets_allowed, ::this.changePets), '\u00A0']}

                {amenities != undefined &&
                    [amenitiesFilter(amenities, this.props.constants.amenities, ::this.updateFilter), '\u00A0']}

                {nofeeonly != undefined &&
                    [nofeeonlyFilter(nofeeonly, ::this.toggleFilter), '\u00A0']}

                {owner_pays != undefined &&
                    [owner_paysFilter(owner_pays, ::this.toggleFilter), '\u00A0']}

                {exclusive != undefined &&
                    [exclusiveFilter(exclusive, ::this.toggleFilter), '\u00A0']}

                {vacant != undefined &&
                    [vacantFilter(vacant, ::this.toggleFilter), '\u00A0']}

                {draft_listings != undefined &&
                    [draft_listingsFilter(draft_listings, ::this.toggleFilter), '\u00A0']}

{/* BELOW NOT IMPLEMENTED YET */}
                {sales_agents != undefined &&
                    [sales_agentsFilter(sales_agents, ::this.voidFunc), '\u00A0']}

                {listing_agents != undefined &&
                    [listing_agentsFilter(listing_agents, ::this.voidFunc), '\u00A0']}

                {hoods != undefined &&
                    [hoodsFilter(hoods, ::this.voidFunc), '\u00A0']}

                {price_per_bed != undefined &&
                    [price_per_bedFilter(price_per_bed, ::this.voidFunc), '\u00A0']}

                {listing_type != undefined &&
                    [listing_typeFilter(listing_type, ::this.voidFunc), '\u00A0']}

                {listing_id != undefined &&
                    [listing_idFilter(listing_id, ::this.voidFunc), '\u00A0']}

                {size != undefined &&
                    [sizeFilter(size, ::this.voidFunc), '\u00A0']}

                {status != undefined &&
                    [statusFilter(status, ::this.voidFunc), '\u00A0']}

                {date_available != undefined &&
                    [date_availableFilter(date_available, ::this.voidFunc), '\u00A0']}

            </ButtonToolbar>
        )
    }
}
