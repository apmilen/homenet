import React from 'react'

import {FormControl, DropdownButton} from 'react-bootstrap'
import {
    Button, ButtonToolbar, InputGroup, InputGroupText, FormRadio, FormCheckbox,
    DatePicker
} from "shards-react";



const searchingText = (searching_text, func) =>
    <div style={{width: '20vw', minWidth: 180}}>
        <FormControl id='searching_text' size="sm"
                     type='text'
                     value={searching_text}
                     placeholder='Search for something you like :)'
                     onChange={func} />
    </div>

const priceFilter = (price, func) =>
    <DropdownButton title='Price'>
        <InputGroup style={{width: 300, margin: '0 5px'}}>
            <InputGroupText>Min:</InputGroupText>
            <FormControl id='price_min' xs='3' step='100'
                         name='price'
                         type='number' min='0' max={price[1]}
                         value={price[0]}
                         onChange={func}
                         placeholder='0'/>&nbsp;

            <InputGroupText>Max:</InputGroupText>
            <FormControl id='price_max' xs='3' step='100'
                         name='price'
                         type='number' min={price[0] || 0}
                         value={price[1]}
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
            <FormRadio name='pets_allowed' value='any'
                       checked={pets_allowed == 'any'}
                       onChange={func} >
            Any
            </FormRadio>
            {Object.keys(pets_allowed_dict).map(allowed_type =>
                <FormRadio name='pets_allowed' value={allowed_type}
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

const listing_idFilter = (listing_id, func) =>
    <div style={{width: '14vw', minWidth: 100}}>
        <FormControl id='listing_id' size="sm"
                     type='text'
                     value={listing_id}
                     placeholder='Listing ID'
                     onChange={func} />
    </div>

const listing_typeFilter = (listing_type, listing_type_dict, func) =>
    <DropdownButton title='Listing Type'>
        <div className='pets-container'>
            <FormRadio name='listing_type' value='any'
                       checked={listing_type == 'any'}
                       onChange={func} >
            Any
            </FormRadio>
            {Object.keys(listing_type_dict).map(lt_type =>
                <FormRadio name='listing_type' value={lt_type}
                           checked={listing_type == lt_type}
                           onChange={func} >
                {listing_type_dict[lt_type]}
                </FormRadio>
            )}
        </div>
    </DropdownButton>

const date_availableFilter = (date_available, func) =>
    <DatePicker selected={date_available}
                onChange={func}
                placeholderText="Date available"
                minDate={new Date()}
                dateFormat="MMMM d, yyyy" />

const price_per_bedFilter = (price_per_bed, func) =>
    <DropdownButton title='Price per Bed'>
        <InputGroup style={{width: 300, margin: '0 5px'}}>
            <InputGroupText>Min:</InputGroupText>
            <FormControl id='price_per_bed_min' xs='3' step='100'
                         name='price_per_bed'
                         type='number' min='0' max={price_per_bed[1]}
                         value={price_per_bed[0]}
                         onChange={func}
                         placeholder='0'/>&nbsp;

            <InputGroupText>Max:</InputGroupText>
            <FormControl id='price_per_bed_max' xs='3' step='100'
                         name='price_per_bed'
                         type='number' min={price_per_bed[0]}
                         value={price_per_bed[1]}
                         onChange={func}
                         placeholder='9999'/>
        </InputGroup>
    </DropdownButton>

const sizeFilter = (size, func) =>
    <DropdownButton title='Square Feet'>
        <InputGroup style={{width: 300, margin: '0 5px'}}>
            <InputGroupText>Min:</InputGroupText>
            <FormControl id='size_min' xs='3' step='100'
                         name='size'
                         type='number' min='0' max={size[1]}
                         value={size[0]}
                         onChange={func}
                         placeholder='min sq.ft'/>&nbsp;

            <InputGroupText>Max:</InputGroupText>
            <FormControl id='size_max' xs='3' step='100'
                         name='size'
                         type='number' min={size[0]}
                         value={size[1]}
                         onChange={func}
                         placeholder='max sq.ft'/>
        </InputGroup>
    </DropdownButton>


const sales_agentsFilter = (sales_agent, func) =>
    <div></div>

const listing_agentsFilter = (listing_agent, func) =>
    <div></div>

const hoodsFilter = (hoods, func) =>
    <div></div>



export class FiltersBar extends React.Component {
    constructor(props) {
        super(props)
        this.state = props.filters
    }
    filtering(e) {
        this.setState({ [e.target.id]: e.target.value }, this.fetchListings)
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
    filterOneSelection (e) {
        const f_name = e.target.getAttribute('name')
        const f_value = e.target.getAttribute('value')
        this.setState({ [f_name]: f_value }, this.fetchListings)
    }
    filterToggle(e) {
        const f_name = e.target.getAttribute('name')
        this.setState({ [f_name]: !this.state[f_name] }, this.fetchListings)
    }
    filterRange(e) {
        const f_name = e.target.getAttribute('name')
        const range = [$('#'+f_name+'_min').val(), $('#'+f_name+'_max').val()]
        this.setState({ [f_name]: range }, this.fetchListings)
    }
    changeDate(date) {
        this.setState({ date_available: date || '' }, this.fetchListings)
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
            searching_text, address, unit, price, beds, baths,
            pets_allowed, amenities, nofeeonly, owner_pays, exclusive, vacant,
            draft_listings,

            sales_agents, listing_agents, hoods, price_per_bed,
            listing_type, listing_id, size, date_available
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
