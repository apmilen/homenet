import React from 'react'
import ReactDOM from 'react-dom'

import {FiltersBar} from '@/pages/filters'


class ListingComponent extends React.Component {
    render() {
        const {
            full_address, no_fee_listing, detail, detail_link, default_image,
            price, price_per_bed, bedrooms, bathrooms, neighborhood, short_id,
            date_available, utilities, move_in_cost, size, landlord_contact,
            listing_agent, sales_agent, owner_pays, agent_notes, agent_bonus,
            pets, term, created, modified, status
        } = this.props.listing

        const {
            listing_status
        } = this.props.constants

        return (
            <div class="row">
              <div class="col-12">
                <div id="main-listing">
                  <div class="container-fluid new-listing-card">
                    <div class="row listing-admin-area">
                      <div class="col-12">
                        <button type="button" class="btn btn-sm btn-outline-info mr-1">{ full_address }</button>
                        <button type="button" class="btn btn-sm btn-outline-info mr-1">Manage</button>
                        <button type="button" class="btn btn-sm btn-outline-info mr-1">Add to Listing Collection</button>
                        { no_fee_listing && <span class="badge badge-info">No fee</span> }&nbsp;
                        { detail.vacant && <span class="badge badge-info">Vacant</span> }
                      </div>
                    </div>
                    <div class="row listing-area-content">
                      <div class="col-lg-4 listing-area-main">
                        <div class="row" style={{ position: 'relative', paddingTop: '56.25%' }}>
                          <a href={ detail_link } target="_blank" rel="noreferrer noopener">
                            <img class="lazy img-fluid mx-auto" s
                                 src={ default_image }
                                 width="960"
                                 height="540"
                                 style={{ position: 'absolute', top: 0, left: 0, width: '100%', height: '100%' }} />
                          </a>
                        </div>
                        <div class="row">
                          <div class="listing-card-stub container-fluid">
                            <div class="row">
                              <div class="col-6">
                                <span>${ price }</span>
                              </div>
                              <div class="col-6">
                                <span>${ price_per_bed }/bed</span>
                              </div>
                            </div>
                            <div class="row">
                              <div class="col-6">
                                <i class="fa fa-bed"></i> { bedrooms } Bed
                              </div>
                              <div class="col-6">
                                <i class="fa fa-bath"></i> { bathrooms } Bath
                              </div>
                            </div>
                            <div class="row">
                              <div class="col-12">
                                <i class="material-icons">place</i>
                                <a href={ detail_link }>
                                  { full_address }
                                </a>
                              </div>
                            </div>
                            <div class="row">
                              <div class="col-12">
                                { neighborhood }
                              </div>
                            </div>
                            <div class="row">
                              <div class="col-12">Subways</div>
                            </div>
                            <div class="row">
                              <div class="col-12 border-bottom-0">Streets</div>
                            </div>
                          </div>
                        </div>
                      </div>
                      <div class="col-lg-4 listing-first-data-col">
                        <div class="row listing-area-data-row">
                          <div class="col-sm-4 text-left"><b>ID</b></div>
                          <div class="col-sm-8 text-left">{ short_id }</div>
                        </div>
                        <div class="row listing-area-data-row">
                          <div class="col-sm-4 text-left"><b>Date Available</b></div>
                          <div class="col-sm-8 text-left">{ date_available }</div>
                        </div>
                        <div class="row listing-area-data-row">
                          <div class="col-sm-4 text-left"><b>Access</b></div>
                          <div class="col-sm-8 text-left">{ detail.building_access }</div>
                        </div>
                        <div class="row listing-area-data-row">
                          <div class="col-sm-4 text-left"><b>Utilities</b></div>
                          <div class="col-sm-8 text-left">{ utilities }</div>
                        </div>
                        <div class="row listing-area-data-row">
                          <div class="col-sm-4 text-left"><b>Move in Cost</b></div>
                          <div class="col-sm-8 text-left">{ move_in_cost }</div>
                        </div>
                        <div class="row listing-area-data-row">
                          <div class="col-sm-4 text-left"><b>Square Feet</b></div>
                          <div class="col-sm-8">{ size }</div>
                        </div>
                        <div class="row listing-area-data-row">
                          <div class="col-sm-4"><b>Landlord</b></div>
                          <div class="col-sm-8">{ detail.landlord_contact }</div>
                        </div>
                        <div class="row text-center">
                          <div class="col-6">
                            <h6>Listing</h6>
                            <a class="contact-avatar" href={ listing_agent.profile_link } target="_blank">
                                <div class="circle-avatar" style={{ backgroundImage: `url(${ listing_agent.avatar_url })`}}></div>
                            </a>
                            { listing_agent.first_name } { listing_agent.last_name }
                          </div>
                          <div class="col-6">
                            <h6>Sales</h6>
                            <a class="contact-avatar" href={ sales_agent.profile_link } target="_blank">
                                <div class="circle-avatar" style={{ backgroundImage: `url(${ sales_agent.avatar_url })`}}></div>
                            </a>
                            { sales_agent.first_name } { sales_agent.last_name }
                          </div>
                          <hr/>
                        </div>
                      </div>
                      <div class="col-lg-4 listing-second-data-col">
                        <div class="row listing-area-data-row">
                          <div class="col-sm-4 text-left"><b>Owner Pays</b></div>
                          <div class="col-sm-8 text-left">{ owner_pays }%</div>
                        </div>
                        <div class="row listing-area-data-row">
                          <div class="col-sm-4 text-left"><b>Agent Notes</b></div>
                          <div class="col-sm-8 text-left">{ agent_notes }</div>
                        </div>
                        <div class="row listing-area-data-row">
                          <div class="col-sm-4 text-left"><b>Agent Bonus</b></div>
                          <div class="col-sm-8 text-left">{ agent_bonus }</div>
                        </div>
                        <div class="row listing-area-data-row">
                          <div class="col-sm-4 text-left"><b>Pets</b></div>
                          <div class="col-sm-8 text-left">{ pets }</div>
                        </div>
                        <div class="row listing-area-data-row">
                          <div class="col-sm-4 text-left"><b>Term</b></div>
                          <div class="col-sm-8 text-left">{ term }</div>
                        </div>
                        <div class="row listing-area-data-row">
                          <div class="col-sm-4 text-left"><b>Created</b></div>
                          <div class="col-sm-8 text-left">{ created }</div>
                        </div>
                        <div class="row listing-area-data-row">
                          <div class="col-sm-4 text-left"><b>Updated</b></div>
                          <div class="col-sm-8 text-left">{ modified }</div>
                        </div>
                        <div class="row listing-area-data-row">
                          <div class="col-sm-4 text-left"><b>Share</b></div>
                          <div class="col-sm-8 text-left">
                              <button class="btn btn-pill btn-outline-info">
                                Copy to Clipboard
                              </button>
                          </div>
                        </div>
                        <div class="row listing-area-data-row border-bottom-0">
                          <div class="col-sm-4 text-left"><b>Status</b></div>
                          <div class="col-sm-8 text-left">{ status }</div>
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


class Listings extends React.Component {
    constructor(props) {
        super(props)
        this.state = {
            filters: {
                searching_text: '',
                price_min: '',
                price_max: '',
                beds: [],
                baths: [],
                pets_allowed: 'any',
                nofeeonly: false,
                amenities: [],
                draft_listings: false,
            },
            'listings': [],
        }
    }
    render() {
        const {constants} = this.props
        const {listings, filters} = this.state

        return (
            <div class="row">
                <div class="col-12 col-md-10 offset-md-1">
                    <div class="page-header row no-gutters py-4 mb-3 border-bottom text-center">
                        <div class="col-12 text-center mb-0">
                            <h3 class="page-title">Manage Listings</h3>
                        </div>
                    </div>
                    <FiltersBar filters={filters} constants={constants}
                                updateParentState={new_state => this.setState(new_state)} />
                    <div class="card card-small mb-4">
                        <ul class="list-group list-group-flush">
                            <li class="list-group-item p-3">
                                <div class="row">
                                    <div class="col">
                                        {listings.map(listing => [
                                            <ListingComponent listing={listing} constants={constants}/>,
                                            <hr class="listings-hr" />
                                        ])}
                                        {!listings &&
                                            <h4>No listings yet.</h4>
                                        }
                                    </div>
                                </div>
                            </li>
                      </ul>
                    </div>
                </div>
            </div>
        )
    }
}

ReactDOM.render(
    React.createElement(Listings, global.props),
    global.react_mount,
)
