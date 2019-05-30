import React from 'react'

import {FormControl, DropdownButton} from 'react-bootstrap'
import {
    Button, ButtonToolbar, InputGroup, InputGroupText, FormRadio, FormCheckbox
} from "shards-react";


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
    toggleFee() {
        this.setState({ nofeeonly: !this.state.nofeeonly }, this.filterListings)
    }
    toggleDrafts() {
        this.setState({ draft_listings: !this.state.draft_listings }, this.filterListings)
    }
    filterListings() {
        this.props.updateParentState({filters: this.state})
        $.get(this.props.endpoint, this.state, (resp) =>
            this.props.updateParentState({listings: resp.results})
        )
    }
    componentDidMount() {
        this.filterListings()
    }
    render() {
        const {
            searching_text, price_min, price_max,
            beds, baths, pets_allowed, nofeeonly, amenities, draft_listings
        } = this.state

        return (
            <ButtonToolbar style={{padding: 5}}>
                <div style={{width: '20vw', minWidth: 180}}>
                    <FormControl id='searching_text' size="sm"
                                 type='text'
                                 value={searching_text}
                                 placeholder='Search for something you like :)'
                                 onChange={::this.filtering} />
                </div>
                &nbsp;
                <DropdownButton title='Price'>
                    <InputGroup style={{width: 300}}>
                        <InputGroupText>Min:</InputGroupText>
                        <FormControl id='price_min' xs='3' step='100'
                                     type='number' min='0' max={price_max}
                                     value={price_min}
                                     onChange={::this.filtering}
                                     placeholder='0'/>&nbsp;

                        <InputGroupText>Max:</InputGroupText>
                        <FormControl id='price_max' xs='3' step='100'
                                     type='number' min={price_min}
                                     value={price_max}
                                     onChange={::this.filtering}
                                     placeholder='9999'/>
                    </InputGroup>
                </DropdownButton>
                &nbsp;
                <DropdownButton title='Bedrooms'>
                    <div className='rooms-container'>
                        {["0", "1", "2", "3", "4+"].map(n_beds =>
                            <div id={n_beds} name='beds'
                                 className={`room-div ${beds.includes(n_beds) ? 'selected' : ''}`}
                                 onClick={::this.updateFilter}>
                                {n_beds}
                            </div>
                        )}
                    </div>
                </DropdownButton>
                &nbsp;
                <DropdownButton title='Baths'>
                    <div className='rooms-container'>
                        {["0", "1", "2", "3+"].map(n_baths =>
                            <div id={n_baths} name='baths'
                                 className={`room-div ${baths.includes(n_baths) ? 'selected' : ''}`}
                                 onClick={::this.updateFilter}>
                                {n_baths}
                            </div>
                        )}
                    </div>
                </DropdownButton>
                &nbsp;
                <DropdownButton title='Pets'>
                    <div className='pets-container'>
                        <FormRadio
                            name='any'
                            checked={pets_allowed == 'any'}
                            onChange={::this.changePets} >
                        Any
                        </FormRadio>
                        {Object.keys(this.props.constants.pets_allowed).map(allowed_type =>
                            <FormRadio
                                name={allowed_type}
                                checked={pets_allowed == allowed_type}
                                onChange={::this.changePets} >
                            {this.props.constants.pets_allowed[allowed_type]}
                            </FormRadio>
                        )}
                    </div>
                </DropdownButton>
                &nbsp;
                <DropdownButton title='Amenities'>
                    <div className='amenities-container'>
                        {Object.keys(this.props.constants.amenities).map(amenity =>
                            <FormCheckbox id={amenity} name="amenities"
                                          checked={amenities.includes(amenity)}
                                          onChange={::this.updateFilter}>
                                {this.props.constants.amenities[amenity]}
                            </FormCheckbox>
                        )}
                    </div>
                </DropdownButton>
                &nbsp;
                <Button outline={!nofeeonly} onClick={::this.toggleFee}>
                    No Fee Only
                </Button>
                &nbsp;
                {draft_listings != undefined &&
                    <Button outline={!draft_listings} onClick={::this.toggleDrafts}>
                        Draft Listings
                    </Button>
                }
            </ButtonToolbar>
        )
    }
}
