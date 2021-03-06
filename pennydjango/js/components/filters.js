import React from 'react'

import {FormControl, DropdownButton, Tabs, Tab} from 'react-bootstrap'
import {
    Button, ButtonToolbar, InputGroup, InputGroupText, FormRadio, FormCheckbox,
    DatePicker
} from "shards-react"



// Text input filters
const formControlStyle = {
    position: 'absolute',
    width: 'inherit',
    minWidth: 'inherit'
}

const textInputClearFilter = (func, elem_id) =>
    <button class="close" style={{height: '100%', padding: '0 6px'}}>
        <span name={elem_id} onClick={(e) => {
            $(`#${elem_id}`).focus()
            func(e)
        }}>&times;</span>
    </button>

export const searchingText = (searching_text, func) =>
    <div style={{width: '20vw', minWidth: 180, height: '100%'}}>
        <FormControl name='searching_text' size="sm"
                     type='text' id='searching_text'
                     value={searching_text}
                     placeholder='Search for something you like :)'
                     style={formControlStyle}
                     onChange={func} />
        {searching_text && textInputClearFilter(func, 'searching_text')}
    </div>

export const addressFilter = (address, func) =>
    <div style={{width: '14vw', minWidth: 100, height: '100%'}}>
        <FormControl name='address' size="sm"
                     type='text' id='address'
                     value={address}
                     placeholder='Address'
                     style={formControlStyle}
                     onChange={func} />
        {address && textInputClearFilter(func, 'address')}
    </div>

export const unitFilter = (unit, func) =>
    <div style={{width: '6vw', minWidth: 50, height: '100%'}}>
        <FormControl name='unit' size="sm"
                     type='text' id='unit'
                     value={unit}
                     placeholder='Unit'
                     style={formControlStyle}
                     onChange={func} />
        {unit && textInputClearFilter(func, 'unit')}
    </div>

export const listing_idFilter = (listing_id, func) =>
    <div style={{width: '14vw', minWidth: 100, height: '100%'}}>
        <FormControl name='listing_id' size="sm"
                     type='text' id='listing_id'
                     value={listing_id}
                     placeholder='Listing ID'
                     style={formControlStyle}
                     onChange={func} />
        {listing_id && textInputClearFilter(func, 'listing_id')}
    </div>

export const lease_idFilter = (lease_id, func) =>
    <div style={{width: '14vw', minWidth: 100, height: '100%'}}>
        <FormControl name='lease_id' size="sm"
                     type='text' id='lease_id'
                     value={lease_id}
                     placeholder='Lease ID'
                     style={formControlStyle}
                     onChange={func} />
        {lease_id && textInputClearFilter(func, 'lease_id')}
    </div>

// Range input filters
const rangeTitle = (title, range, pre='', pos='') =>
`${title}${
    range[0] ? 
    (range[1] ? `: ${pre}${range[0]}${pos} -` : ` from ${pre}${range[0]}${pos}`) : ''
}${
    range[1] ?
    (range[0] ? ` ${pre}${range[1]}${pos}` : ` up to ${pre}${range[1]}${pos}`) : ''
}`

const validRange = (range) => range.length == 2 && (range[0] || range[1])

const rangeClearFilter = (func, elem_id) =>
    <span name={elem_id} className='times' onClick={(e) => {
        e.stopPropagation()
        $(`#${elem_id}_min`).val("")
        $(`#${elem_id}_max`).val("")
        func(e)
    }}>&times;</span>

export const priceFilter = (price, func) =>
    <DropdownButton alignRight title={[rangeTitle("Price", price, '$'),
                            validRange(price) && rangeClearFilter(func, "price")]}
                    className={validRange(price) ? 'no-caret' : ''}>
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
    <DropdownButton alignRight title={[rangeTitle("Price per Bed", price_per_bed, '$'),
                            validRange(price_per_bed) && rangeClearFilter(func, "price_per_bed")]}
                    className={validRange(price_per_bed) ? 'no-caret' : ''}>
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
                         type='number' min={price_per_bed[0] || 0}
                         value={price_per_bed[1]}
                         onChange={func}
                         placeholder='9999'/>
        </InputGroup>
    </DropdownButton>

export const sizeFilter = (size, func) =>
    <DropdownButton alignRight title={[rangeTitle("Size", size, '', 'sq.ft'),
                            validRange(size) && rangeClearFilter(func, "size")]}
                    className={validRange(size) ? 'no-caret' : ''}>
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
const multipleSelectionTitle = (title, list) =>
    `${title}${list.length ? `: ${list.length} selected` : ''}`

const multipleSelectionClearFilter = (func, elem_id) =>
    <span name={elem_id} className='times' onClick={(e) => {
        e.stopPropagation()
        func(e, elem_id, [])
    }}>&times;</span>

export const bedsFilter = (beds, func) =>
    <DropdownButton alignRight title={[`Bedrooms${beds.length ? `: ${beds.sort()}` : ''}`,
                            beds.length > 0 && multipleSelectionClearFilter(func, "beds")]}
                    className={beds.length > 0 ? 'no-caret' : ''}>
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
    <DropdownButton alignRight title={[`Bathrooms${baths.length ? `: ${baths.sort()}` : ''}`,
                            baths.length > 0 && multipleSelectionClearFilter(func, "baths")]}
                    className={baths.length > 0 ? 'no-caret' : ''}>
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
    <DropdownButton alignRight title={[multipleSelectionTitle("Amenities", amenities),
                            amenities.length > 0 && multipleSelectionClearFilter(func, "amenities")]}
                    className={`${amenities.length > 0 ? 'no-caret' : ''}`}>
        <div className='dropdown-checkbox-container'>
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
    <DropdownButton alignRight title={[multipleSelectionTitle("Sales Agents", sales_agents),
                            sales_agents.length > 0 && multipleSelectionClearFilter(func, "sales_agents")]}
                    className={sales_agents.length > 0 ? 'no-caret' : ''}>
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
    <DropdownButton alignRight title={[multipleSelectionTitle("Listing Agents", listing_agents),
                            listing_agents.length > 0 && multipleSelectionClearFilter(func, "listing_agents")]}
                    className={listing_agents.length > 0 ? 'no-caret' : ''}>
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

const hoodsList = (borough_hoods, hoods) => {
    const has_all_hoods = borough_hoods.every(hood => hoods.includes(hood[0]))
    const has_no_hoods = borough_hoods.every(hood => !hoods.includes(hood[0]))
    if (has_all_hoods || has_no_hoods)
        return borough_hoods.map(hood => hood[0])
    else
        return borough_hoods.filter(hood => !hoods.includes(hood[0])).map(hood => hood[0])
}

export const hoodsFilter = (hoods, hoods_dict, func) =>
    <DropdownButton alignRight title={[multipleSelectionTitle("Hoods", hoods),
                            hoods.length > 0 && multipleSelectionClearFilter(func, "hoods")]}
                    className={` ${hoods.length > 0 ? 'no-caret' : ''}`}>
        <div className='borough-container'>
            <Tabs defaultActiveKey={0}>
                {Object.keys(hoods_dict).map((borough, idx) =>
                    <Tab eventKey={idx} title={borough} key={`${borough}-borough`}>
                        <div className='hoods-container'>

                            <FormCheckbox id={`all-${borough}`} key={`all-${borough}`}
                                          checked={hoods_dict[borough].every(hood => hoods.includes(hood[0]))}
                                          onChange={e => func(e, "hoods", hoodsList(hoods_dict[borough], hoods))}>
                                {`${hoods_dict[borough].every(hood => hoods.includes(hood[0])) ? 'Unselect' : 'Select'} all`}
                            </FormCheckbox>
                            <br/>
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

export const lease_statusFilter = (lease_status, status_dict, func) =>
    <DropdownButton alignRight title={[multipleSelectionTitle("Status", lease_status),
                            lease_status.length > 0 && multipleSelectionClearFilter(func, "lease_status")]}
                    className={lease_status.length > 0 ? 'no-caret' : ''}>
        <div className='agents-container'>
            {status_dict.map(status =>
                <FormCheckbox id={status[0]} key={`${status[0]}-lease-status`}
                              checked={lease_status.includes(status[0])}
                              onChange={e => func(e, "lease_status")}>
                    {status[1]}
                </FormCheckbox>
            )}
        </div>
    </DropdownButton>

// One selection filters
export const pets_allowedFilter = (pets_allowed, pets_allowed_dict, func) =>
    <DropdownButton alignRight className=""
                    title={`Pets: ${pets_allowed == 'any' ? "Any" : pets_allowed_dict[pets_allowed]}`}>
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
    <DropdownButton alignRight title={`Listing Type: ${listing_type == 'any' ? "Any" : listing_type_dict[listing_type]}`}>
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

export const user_typeFilter = (user_type, user_type_dict, func) =>
    <DropdownButton alignRight title={`User Type: ${user_type == 'any' ? "Any" : user_type_dict[user_type]}`}>
        <div className='pets-container'>
            <FormRadio name='user_type' value='any'
                       checked={user_type == 'any'}
                       onChange={func} >
            Any
            </FormRadio>
            {Object.keys(user_type_dict).map(u_type =>
                <FormRadio key={`${u_type}-user-type`}
                           name='user_type' value={u_type}
                           checked={user_type == u_type}
                           onChange={func} >
                {user_type_dict[u_type]}
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

export const only_activeFilter = (only_active, func) =>
    <Button outline={!only_active} onClick={func} name="only_active">
        Only active
    </Button>

// Date filters
export const date_availableFilter = (date_available, func) =>
    <DatePicker selected={date_available}
                onChange={func}
                placeholderText="Date available"
                minDate={new Date()}
                dateFormat="MMMM d, yyyy"
                style={{width: '40vw'}} />
