import React from 'react'

export const Lease = ({lease}) => {
    const listing = lease.listing
    return <div className="row">
        <div className="col-12">
            <div id="main-listing">
                <div className="container-fluid new-listing-card">
                    <div className="row listing-admin-area">
                        <div className="col-12">
                            <button type="button"
                                    className="btn btn-sm btn-outline-info mr-1">
                                {lease.listing.address}
                            </button>
                            <button type="button"
                                    className="btn btn-sm btn-outline-info mr-1">Manage
                            </button>
                            <button type="button"
                                    className="btn btn-sm btn-outline-info mr-1">Listing
                            </button>
                        </div>
                    </div>
                    <div className="row listing-area-content">
                        <div className="col-lg-4 listing-area-main">
                            <div className="row"
                                 style={{position: 'relative', paddingTop: '56.25%'}}>
                                <a href={`${lease.detail_link}`}
                                   target="_blank" rel="noreferrer noopener">
                                    <img className="lazy img-fluid mx-auto"
                                         src={`${listing.default_image}`}
                                         width="960"
                                         height="540"
                                         style={{position: 'absolute', top: '0', left: '0', width: '100%', height: '100%'}}/>
                                </a>
                            </div>
                            <div className="row">
                                <div className="listing-card-stub container-fluid">
                                </div>
                            </div>
                        </div>
                        <div className="col-lg-4 listing-first-data-col">
                            <div className="row listing-area-data-row">
                                <div className="col-sm-4 text-left"><b>Status</b>
                                </div>
                                <div className="col-sm-8 text-left">
                                    {lease.status}
                                </div>
                            </div>
                            <div className="row listing-area-data-row">
                                <div className="col-sm-4 text-left"><b>ID</b>
                                </div>
                                <div className="col-sm-8 text-left">
                                    {lease.short_id}
                                </div>
                            </div>
                            <div className="row listing-area-data-row">
                                <div className="col-sm-4 text-left">
                                    <b>Neighborhood</b>
                                </div>
                                <div className="col-sm-8 text-left">
                                    {listing.neighborhood}
                                </div>
                            </div>
                            <div className="row listing-area-data-row">
                                <div className="col-sm-4 text-left">
                                    <b>Site apply</b>
                                </div>
                                <div className="col-sm-8 text-left">
                                    TODO
                                </div>
                            </div>
                            <div className="row listing-area-data-row">
                                <div className="col-sm-4 text-left">
                                    <b>Rent</b>
                                </div>
                                <div className="col-sm-8 text-left">
                                    {listing.price}
                                </div>
                            </div>
                            <div className="row listing-area-data-row">
                                <div className="col-sm-4 text-left">
                                    <b>Offer</b>
                                </div>
                                <div className="col-sm-8 text-left">
                                    {lease.offer || 'N/A'}
                                </div>
                            </div>
                            <div className="row listing-area-data-row">
                                <div className="col-sm-4 text-left">
                                    <b>Term</b>
                                </div>
                                <div className="col-sm-8 text-left">
                                    {lease.length_of_lease} Months
                                </div>
                            </div>
                            <div className="row listing-area-data-row">
                                <div className="col-sm-4 text-left">
                                    <b>Broker Fee</b>
                                </div>
                                <div className="col-sm-8 text-left">
                                    {lease.total_broker_fee || 'N/A'}
                                </div>
                            </div>
                            <div className="row listing-area-data-row">
                                <div className="col-sm-4 text-left">
                                    <b>Owner Pays</b>
                                </div>
                                <div className="col-sm-8 text-left">
                                    {lease.op}%
                                </div>
                            </div>
                            <div className="row listing-area-data-row">
                                <div className="col-sm-4 text-left">
                                    <b>Office</b>
                                </div>
                                <div className="col-sm-8 text-left">

                                </div>
                            </div>
                        </div>
                        <div className="col-lg-4 listing-second-data-col">
                            <div className="row listing-area-data-row">
                                <div className="col-sm-4 text-left">
                                    <b>Move In</b>
                                </div>
                                <div className="col-sm-8 text-left">
                                    {lease.move_in_date}
                                </div>
                            </div>
                            <div className="row listing-area-data-row">
                                <div className="col-sm-4 text-left">
                                    <b>Credit Checks</b>
                                </div>
                                <div className="col-sm-8 text-left">
                                    TODO
                                </div>
                            </div>
                            <div className="row listing-area-data-row">
                                <div className="col-sm-4 text-left">
                                    <b>Description</b>
                                </div>
                                <div className="col-sm-8 text-left">
                                    TODO
                                </div>
                            </div>
                            <div className="row listing-area-data-row">
                                <div className="col-sm-4 text-left">
                                    <b>Transactions</b>
                                </div>
                                <div className="col-sm-8 text-left">
                                    TODO
                                </div>
                            </div>
                            <div className="row listing-area-data-row">
                                <div className="col-sm-4 text-left">
                                    <b>Current Balance</b>
                                </div>
                                <div className="col-sm-8 text-left">
                                    TODO
                                </div>
                            </div>
                            <div className="row listing-area-data-row">
                                <div className="col-sm-4 text-left">
                                    <b>OP Received at</b>
                                </div>
                                <div className="col-sm-8 text-left">
                                    TODO
                                </div>
                            </div>
                            <div className="row listing-area-data-row">
                                <div className="col-sm-4 text-left">
                                    <b>Client Name</b>
                                </div>
                                <div className="col-sm-8 text-left">
                                    TODO
                                </div>
                            </div>
                            <div className="row listing-area-data-row">
                                <div className="col-sm-4 text-left">
                                    <b>Created By</b>
                                </div>
                                <div className="col-sm-8 text-left">
                                    {lease.created_by}
                                </div>
                            </div>
                            <div className="row listing-area-data-row">
                                <div className="col-sm-4 text-left">
                                    <b>Created at</b>
                                </div>
                                <div className="col-sm-8 text-left">
                                    {lease.created}
                                </div>
                            </div>
                            <div className="row listing-area-data-row">
                                <div className="col-sm-4 text-left">
                                    <b>Updated at</b>
                                </div>
                                <div className="col-sm-8 text-left">
                                    {lease.modified}
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
}
