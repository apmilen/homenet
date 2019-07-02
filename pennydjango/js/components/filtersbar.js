import React from 'react'

import {ButtonToolbar, Button, Collapse, Col, Row} from "shards-react";

import {
    searchingText, addressFilter, unitFilter, priceFilter, price_per_bedFilter,
    bedsFilter, bathsFilter, listing_typeFilter, listing_idFilter, sizeFilter,
    pets_allowedFilter, amenitiesFilter, nofeeonlyFilter, owner_paysFilter,
    exclusiveFilter, vacantFilter, draft_listingsFilter, date_availableFilter,
    sales_agentsFilter, listing_agentsFilter, hoodsFilter, lease_idFilter,
    lease_statusFilter
} from "./filters"
import {ALL_FILTERS} from '@/constants'


export class FiltersBar extends React.Component {
    constructor(props) {
        super(props)
        let initial_filters = {}
        props.filters.concat(props.advancedFilters).map(filter_name =>
            initial_filters[filter_name] = props.filtersState && props.filtersState[filter_name] ?
                props.filtersState[filter_name] : ALL_FILTERS[filter_name]
        )
        this.state = {
            filters: initial_filters,
            show_collapse: false,
        }
    }

    updateFilter(filter) {
        this.setState({
            filters: {...this.state.filters, ...filter}
        }, this.updateParent)
    }

    filtering(e) {
        const f_name = e.target.getAttribute('name')
        const f_value = e.target.value || ""
        this.updateFilter({[f_name]: f_value})
    }

    filterMultipleSelection(e, filter_name, values_list) {
        const item_type = filter_name || e.target.getAttribute('name')
        const current_filter = this.state.filters[item_type]
        let new_filter = current_filter

        if (values_list === undefined) {
            const value = e.target.id
            new_filter = current_filter.includes(value) ?
                current_filter.filter(val => val != value) :
                current_filter.concat(value)
        } else if (values_list.length == 0) {
            new_filter = []
        } else {
            new_filter = [
                ...current_filter.filter(val => values_list.indexOf(val) == -1),
                ...values_list.filter(val => current_filter.indexOf(val) == -1)
            ]
        }

        this.updateFilter({[item_type]: new_filter})
    }

    filterOneSelection(e) {
        const f_name = e.target.getAttribute('name')
        const f_value = e.target.getAttribute('value')
        this.updateFilter({[f_name]: f_value})
    }

    filterToggle(e) {
        const f_name = e.target.getAttribute('name')
        this.updateFilter({[f_name]: !this.state.filters[f_name]})
    }

    filterRange(e) {
        const f_name = e.target.getAttribute('name')
        const range = [$(`#${f_name}_min`).val(), $(`#${f_name}_max`).val()]
        this.updateFilter({[f_name]: range})
    }

    changeDate(date) {
        this.updateFilter({date_available: date || ''})
    }

    updateParent() {
        let params = {...this.state.filters}
        if (params.date_available)
            params.date_available = params.date_available.getFullYear() + ' ' +
                                    (params.date_available.getMonth() + 1) + ' ' +
                                    params.date_available.getDate()

        const {updateFilters, updateParams} = this.props
        updateFilters && updateFilters(this.state.filters)
        updateParams && updateParams(params)
    }

    clearFilters(e) {
        let cleaned_filters = {}
        Object.keys(this.state.filters).map(
            f_name => cleaned_filters[f_name] = ALL_FILTERS[f_name]
        )
        this.updateFilter(cleaned_filters)
    }

    componentDidMount() {
        this.updateParent()
    }

    renderFilters(filters) {
        const {
            searching_text, address, unit, sales_agents, listing_agents, hoods,
            price, price_per_bed, beds, baths, listing_type, listing_id, size,
            pets_allowed, amenities, nofeeonly, owner_pays, exclusive, vacant,
            draft_listings, date_available, lease_id, lease_status
        } = filters

        return [
            searching_text != undefined &&
            <div className='filter-container'>{searchingText(searching_text, ::this.filtering)}</div>,

            address != undefined &&
            <div className='filter-container'>{addressFilter(address, ::this.filtering)}</div>,

            unit != undefined &&
            <div className='filter-container'>{unitFilter(unit, ::this.filtering)}</div>,

            sales_agents != undefined &&
            <div className='filter-container'>{sales_agentsFilter(sales_agents, this.props.constants.agents, ::this.filterMultipleSelection)}</div>,

            listing_agents != undefined &&
            <div className='filter-container'>{listing_agentsFilter(listing_agents, this.props.constants.agents, ::this.filterMultipleSelection)}</div>,

            hoods != undefined &&
            <div className='filter-container'>{hoodsFilter(hoods, this.props.constants.neighborhoods, ::this.filterMultipleSelection)}</div>,

            price != undefined &&
            <div className='filter-container'>{priceFilter(price, ::this.filterRange)}</div>,

            price_per_bed != undefined &&
            <div className='filter-container'>{price_per_bedFilter(price_per_bed, ::this.filterRange)}</div>,

            beds != undefined &&
            <div className='filter-container'>{bedsFilter(beds, ::this.filterMultipleSelection)}</div>,

            baths != undefined &&
            <div className='filter-container'>{bathsFilter(baths, ::this.filterMultipleSelection)}</div>,

            listing_type != undefined &&
            <div className='filter-container'>{listing_typeFilter(listing_type, this.props.constants.listing_types, ::this.filterOneSelection)}</div>,

            listing_id != undefined &&
            <div className='filter-container'>{listing_idFilter(listing_id, ::this.filtering)}</div>,

            lease_id != undefined &&
            <div className='filter-container'>{lease_idFilter(lease_id, ::this.filtering)}</div>,

            lease_status != undefined &&
            <div className='filter-container'>{lease_statusFilter(lease_status, this.props.constants.lease_status, ::this.filterMultipleSelection)}</div>,

            size != undefined &&
            <div className='filter-container'>{sizeFilter(size, ::this.filterRange)}</div>,

            pets_allowed != undefined &&
            <div className='filter-container'>{pets_allowedFilter(pets_allowed, this.props.constants.pets_allowed, ::this.filterOneSelection)}</div>,

            amenities != undefined &&
            <div className='filter-container'>{amenitiesFilter(amenities, this.props.constants.amenities, ::this.filterMultipleSelection)}</div>,

            nofeeonly != undefined &&
            <div className='filter-container'>{nofeeonlyFilter(nofeeonly, ::this.filterToggle)}</div>,

            owner_pays != undefined &&
            <div className='filter-container'>{owner_paysFilter(owner_pays, ::this.filterToggle)}</div>,

            exclusive != undefined &&
            <div className='filter-container'>{exclusiveFilter(exclusive, ::this.filterToggle)}</div>,

            vacant != undefined &&
            <div className='filter-container'>{vacantFilter(vacant, ::this.filterToggle)}</div>,

            draft_listings != undefined &&
            <div className='filter-container'>{draft_listingsFilter(draft_listings, ::this.filterToggle)}</div>,

            date_available != undefined &&
            <div className='filter-container'>{date_availableFilter(date_available, ::this.changeDate)}</div>,
        ]
    }

    render() {
        const {filters, show_collapse} = this.state
        const advanced_filters = this.props.advancedFilters
        let basic_filters = {}, extra_filters = {}

        Object.keys(filters).map(filter_name => {
            if ((advanced_filters || []).includes(filter_name))
                extra_filters[filter_name] = filters[filter_name]
            else
                basic_filters[filter_name] = filters[filter_name]
        })

        return <Col>
            <Row className="justify-content-center">
                <ButtonToolbar>
                    {this.renderFilters(basic_filters)}
                    <div className='filter-container'>
                        <Button outline theme="light" onClick={::this.clearFilters}>
                            Clear filters
                        </Button>
                    </div>
                    {advanced_filters &&
                        <div className='filter-container'>
                            <Button outline theme="light" onClick={() => 
                                this.setState({show_collapse: !show_collapse})
                            }>
                                {`+ ${show_collapse ? 'less' : 'more'} filters`}
                            </Button>
                        </div>
                    }
                </ButtonToolbar>
            </Row>
            {advanced_filters &&
                <Row className="justify-content-center">
                    <Collapse open={show_collapse}>
                        <ButtonToolbar>
                            {this.renderFilters(extra_filters)}
                        </ButtonToolbar>
                    </Collapse>
                </Row>
            }
        </Col>
    }
}

