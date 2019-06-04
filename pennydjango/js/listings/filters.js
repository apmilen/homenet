import React from 'react'

import {FormControl, DropdownButton, Tabs, Tab} from 'react-bootstrap'
import {
    Button, ButtonToolbar, InputGroup, InputGroupText, FormRadio, FormCheckbox,
    DatePicker
} from "shards-react";


// Text input filters
export const searchingText = (searching_text, func) =>
    <div style={{width: '20vw', minWidth: 180}}>
        <FormControl id='searching_text' size="sm"
                     type='text'
                     value={searching_text}
                     placeholder='Search for something you like :)'
                     onChange={func} />
    </div>

export const addressFilter = (address, func) =>
    <div style={{width: '14vw', minWidth: 100}}>
        <FormControl id='address' size="sm"
                     type='text'
                     value={address}
                     placeholder='Address'
                     onChange={func} />
    </div>

export const unitFilter = (unit, func) =>
    <div style={{width: '6vw', minWidth: 50}}>
        <FormControl id='unit' size="sm"
                     type='text'
                     value={unit}
                     placeholder='Unit'
                     onChange={func} />
    </div>

export const listing_idFilter = (listing_id, func) =>
    <div style={{width: '14vw', minWidth: 100}}>
        <FormControl id='listing_id' size="sm"
                     type='text'
                     value={listing_id}
                     placeholder='Listing ID'
                     onChange={func} />
    </div>

// Range input filters
export const priceFilter = (price, func) =>
    <DropdownButton title='Price' alignRight>
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

export const price_per_bedFilter = (price_per_bed, func) =>
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

export const sizeFilter = (size, func) =>
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

// Multiple selection filters
export const bedsFilter = (beds, func) =>
    <DropdownButton title='Bedrooms'>
        <div className='rooms-container'>
            {["0", "1", "2", "3", "4+"].map(n_beds =>
                <div id={n_beds} name='beds' key={`${n_beds}-beds`}
                     className={`room-div ${beds.includes(n_beds) ? 'selected' : ''}`}
                     onClick={func}>
                    {n_beds}
                </div>
            )}
        </div>
    </DropdownButton>

export const bathsFilter = (baths, func) =>
    <DropdownButton title='Baths'>
        <div className='rooms-container'>
            {["0", "1", "2", "3+"].map(n_baths =>
                <div id={n_baths} name='baths' key={`${n_baths}-baths`}
                     className={`room-div ${baths.includes(n_baths) ? 'selected' : ''}`}
                     onClick={func}>
                    {n_baths}
                </div>
            )}
        </div>
    </DropdownButton>

export const amenitiesFilter = (amenities, amenities_dict, func) =>
    <DropdownButton title='Amenities' className="dropdown-menu-mobile">
        <div className='amenities-container'>
            {Object.keys(amenities_dict).map(amenity =>
                <FormCheckbox id={amenity} key={`${amenity}-amen`}
                              checked={amenities.includes(amenity)}
                              onChange={e => func(e, "amenities")}>
                    {amenities_dict[amenity]}
                </FormCheckbox>
            )}
        </div>
    </DropdownButton>

export const sales_agentsFilter = (sales_agents, agents, func) =>
    <DropdownButton title="Sales Agents" alignRight>
        <div className='agents-container'>
            {agents.map(agent =>
                <FormCheckbox id={agent[0]} key={`${agent[0]}-sales-agent`}
                              checked={sales_agents.includes(agent[0])}
                              onChange={e => func(e, "sales_agents")}>
                    {agent[1] || `@${agent[0]}`}
                </FormCheckbox>
            )}
        </div>
    </DropdownButton>

export const listing_agentsFilter = (listing_agents, agents, func) =>
    <DropdownButton title="Listing Agents">
        <div className='agents-container'>
            {agents.map(agent =>
                <FormCheckbox id={agent[0]} key={`${agent[0]}-listing-agent`}
                              checked={listing_agents.includes(agent[0])}
                              onChange={e => func(e, "listing_agents")}>
                    {agent[1] || `@${agent[0]}`}
                </FormCheckbox>
            )}
        </div>
    </DropdownButton>

export const hoodsFilter = (hoods, hoods_dict, func) =>
    <DropdownButton title='Hoods' className="dropdown-menu-mobile">
        <div className='borough-container'>
            <Tabs defaultActiveKey={0}>
                {Object.keys(hoods_dict).map((borough, idx) =>
                    <Tab eventKey={idx} title={borough} key={`${borough}-borough`}>
                        <div className='hoods-container'>
                            {hoods_dict[borough].map(hood =>
                                <FormCheckbox id={hood[0]} key={`${hood[0]}-hood`}
                                              checked={hoods.includes(hood[0])}
                                              onChange={e => func(e, "hoods")}>
                                    {hood[1]}
                                </FormCheckbox>
                            )}
                        </div>
                    </Tab>
                )}
            </Tabs>
        </div>
    </DropdownButton>

// One selection filters
export const pets_allowedFilter = (pets_allowed, pets_allowed_dict, func) =>
    <DropdownButton title='Pets' className="dropdown-menu-mobile">
        <div className='pets-container'>
            <FormRadio name='pets_allowed' value='any'
                       checked={pets_allowed == 'any'}
                       onChange={func} >
            Any
            </FormRadio>
            {Object.keys(pets_allowed_dict).map(allowed_type =>
                <FormRadio key={`${allowed_type}-pets`}
                           name='pets_allowed' value={allowed_type}
                           checked={pets_allowed == allowed_type}
                           onChange={func} >
                {pets_allowed_dict[allowed_type]}
                </FormRadio>
            )}
        </div>
    </DropdownButton>

export const listing_typeFilter = (listing_type, listing_type_dict, func) =>
    <DropdownButton title='Listing Type'>
        <div className='pets-container'>
            <FormRadio name='listing_type' value='any'
                       checked={listing_type == 'any'}
                       onChange={func} >
            Any
            </FormRadio>
            {Object.keys(listing_type_dict).map(lt_type =>
                <FormRadio key={`${lt_type}-listing`}
                           name='listing_type' value={lt_type}
                           checked={listing_type == lt_type}
                           onChange={func} >
                {listing_type_dict[lt_type]}
                </FormRadio>
            )}
        </div>
    </DropdownButton>

// Toggle buttons
export const nofeeonlyFilter = (nofeeonly, func) =>
    <Button outline={!nofeeonly} onClick={func} name="nofeeonly">
        No Fee Only
    </Button>

export const draft_listingsFilter = (draft_listings, func) =>
    <Button outline={!draft_listings} onClick={func} name="draft_listings">
        Draft Listings
    </Button>

export const owner_paysFilter = (owner_pays, func) =>
    <Button outline={!owner_pays} onClick={func} name="owner_pays">
        Owner Pays
    </Button>

export const exclusiveFilter = (exclusive, func) =>
    <Button outline={!exclusive} onClick={func} name="exclusive">
        Exclusive
    </Button>

export const vacantFilter = (vacant, func) =>
    <Button outline={!vacant} onClick={func} name="vacant">
        Vacant
    </Button>

// Date filters
export const date_availableFilter = (date_available, func) =>
    <DatePicker selected={date_available}
                onChange={func}
                placeholderText="Date available"
                minDate={new Date()}
                dateFormat="MMMM d, yyyy"
                style={{width: '40vw'}} />
