import React from 'react'

import FormControl from 'react-bootstrap/FormControl'
import DropdownButton from 'react-bootstrap/DropdownButton'
import Modal from 'react-bootstrap/Modal'
import FormGroup from 'react-bootstrap/FormGroup'
import FormLabel from 'react-bootstrap/FormLabel'
import Form from 'react-bootstrap/Form'
import {FormCheckbox} from 'shards-react'
import ClipboardJS from 'clipboard'


const validateCollectionForm = (collection_data) => {
    const {name, notes} = collection_data
    let errors = []
    if (name === "") errors.push("Name cannot be empty")
    if (notes === "") errors.push("Please fill notes with something useful")
    return errors
}

class ChangeStatusModal extends React.Component {
    constructor(props) {
        super(props)
        this.state = {
            show: false,
        }
    }
    toggleModal() {
        this.setState({
            show: !this.state.show,
            status: '',
        })
    }
    handleInput(e) {
        const field = e.target.id
        const value = e.target.value
        this.setState({[field]: value})
    }
    render() {
        const {show} = this.state
        return (
            <span>
                <a className="dropdown-item" href="#" onClick={::this.toggleModal}>
                    <i className={'material-icons'}>settings</i> Change Status
                </a>
                {show &&
                <Modal show={show} size="sm" onHide={::this.toggleModal}>
                    <Modal.Header closeButton>
                        <Modal.Title className="collection-modal-title">
                            Change Status
                        </Modal.Title>
                    </Modal.Header>
                    <Modal.Body className="collection-modal-body">
                        <span>
                            <Form method={"post"} action={this.props.link}>
                                <input type="hidden" name="csrfmiddlewaretoken" value={global.csrftoken} />
                                <FormGroup controlId="id_status" >
                                    <FormLabel>Status</FormLabel>
                                    <FormControl as="select" name={'status'}>
                                      <option value={'draft'}>Draft</option>
                                      <option value={'approved'}>Approved</option>
                                      <option value={'cancelled'}>Cancelled</option>
                                      <option value={'rented'}>Rented</option>
                                    </FormControl>
                                  </FormGroup>
                                <button
                                    className="btn btn-primary"
                                    type={'submit'}>
                                    Submit
                                </button>
                            </Form>
                        </span>
                    </Modal.Body>
                </Modal>}
            </span>
        )
    }
}

class CreateCollectionModal extends React.Component {
    constructor(props) {
        super(props)
        this.state = {
            show: false,
        }
    }
    toggleModal() {
        this.setState({
            show: !this.state.show,
            errors: [],
            name: '',
            notes: '',
        })
    }
    handleInput(e) {
        const field = e.target.id
        const value = e.target.value
        let errors = []
        if (field == "name" && value.length > 32) errors.push("Name too large")
        if (errors.length > 0)
            this.setState({errors})
        else
            this.setState({[field]: value, errors})
    }
    submitCollection() {
        const {show, errors, ...collection_data} = this.state
        const new_errors = validateCollectionForm(collection_data)
        if (new_errors.length)
            this.setState({errors: new_errors})
        else {
            const post_data = {
                type: 'CREATE_COLLECTION',
                listing_id: this.props.listing_id,
                ...collection_data,
            }
            $.post("/listings/", post_data, response => {
                if (response.success)
                    global.location.reload()
                else
                    this.setState({errors: response.errors})
            })
        }
    }
    render() {
        const {show, errors, name, notes} = this.state
        return (
            <span>
                <button
                    className="btn btn-pill btn-outline-secondary w-100"
                    onClick={::this.toggleModal}
                    style={{margin: '5px 0 10px 0'}}>
                    Create collection
                </button>

                {show &&
                <Modal show={show} size="sm" onHide={::this.toggleModal}>
                    <Modal.Header closeButton>
                        <Modal.Title className="collection-modal-title">
                            New collection
                        </Modal.Title>
                    </Modal.Header>
                    <Modal.Body className="collection-modal-body">
                        <span><center>
                            {errors.map((error, i) =>
                                <div key={i} className="collection-modal-error">{error}</div>
                            )}
                            <FormControl id='name' type='text' value={name}
                                         autoComplete="off" required
                                         className="collection-modal-field"
                                         placeholder='Collection name'
                                         onChange={::this.handleInput} />
                            <FormControl id='notes' type='text' value={notes}
                                         autoComplete="off"
                                         className="collection-modal-field"
                                         placeholder='Additional notes'
                                         onChange={::this.handleInput} />
                            <button
                                className="btn btn-pill btn-outline-secondary"
                                onClick={::this.submitCollection}>
                                Create Collection
                            </button>
                        </center></span>
                    </Modal.Body>
                </Modal>}
            </span>
        )
    }
}

const AddToCollection = ({listing_id, agent_collections, listing_collection_ids, onClickCollection}) =>
    <DropdownButton title="Add to collection" className="d-inline mr-1" variant="outline-info" size="sm">
        <div className="dropdown-checkbox-container" style={{width: 160, fontSize: '.813rem'}}>
            <CreateCollectionModal listing_id={listing_id}/>
            {agent_collections.map(collection => {
                const {id, name} = collection
                return (
                    <FormCheckbox id={id} key={`${id}-collection`}
                                  checked={listing_collection_ids.includes(id)}
                                  onChange={onClickCollection}>
                        {name}
                    </FormCheckbox>
                )
            })}
        </div>
    </DropdownButton>


export class ListingComponent extends React.Component {
    constructor(props) {
        super(props)
        this.state = {
            collections: props.listing.collections
        }
    }
    toggleCollection(e) {
        const post_data = {
            type: 'LISTING_COLLECTION',
            collection_id: e.target.id,
            listing_id: this.props.listing.id
        }
        $.post("/listings/", post_data, response => {
            if (response.success) {
                this.setState({collections: response.collections})
            }
        })
    }
    componentDidMount() {
        new ClipboardJS(`#clip-${this.props.listing.id}`)
    }

    render() {
        const {
            full_address, no_fee_listing, detail, detail_link, default_image,
            price, price_per_bed, bedrooms, bathrooms, neighborhood, short_id,
            date_available, utilities, move_in_cost, size, landlord_contact,
            listing_agent, owner_pays, agent_notes, agent_bonus,
            pets, term, created, modified, status, listing_link, edit_link,
            offer_link, nearby_transit, parking, photos_link, id, change_status_link
        } = this.props.listing
        const {
            collections
        } = this.state

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
                                            <a className="dropdown-item" href={photos_link}>
                                                <i className={'material-icons'}>camera</i> Photos
                                            </a>
                                            <div className="dropdown-divider"></div>
                                            <a className="dropdown-item" href={offer_link}>
                                                <i className={'material-icons'}>create_new_folder</i> Create Offer
                                            </a>
                                            <div className="dropdown-divider"></div>
                                            <ChangeStatusModal link={change_status_link}/>
                                        </div>
                                    </div>
                                    <AddToCollection
                                        listing_id={id}
                                        agent_collections={global.user.collections_list}
                                        listing_collection_ids={collections}
                                        onClickCollection={::this.toggleCollection}
                                    />
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
                                        <a href={listing_link} target="_blank"
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
                                                    className="col-12 ">Streets
                                                </div>
                                            </div>
                                            <div className="row border-bottom-0 nearby-transit">
                                                <div className="col-sm-4 text-left"><b>Nearby Transit</b></div>
                                                <div className="col-sm-8 text-left">{nearby_transit}</div>
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
                                            <b>Parking</b></div>
                                        <div className="col-sm-8 text-left">{parking}</div>
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
                                                id={`clip-${id}`}
                                                data-clipboard-text={`${global.props.BASE_URL}${listing_link}`}
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

