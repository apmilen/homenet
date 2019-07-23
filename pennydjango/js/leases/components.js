import React from 'react'

export const Lease = ({lease}) => {
    const listing = lease.listing
    const creator = lease.created_by
    return <div className="row">
        <div className="col-12">
            <div id="main-listing">
                <div className="container-fluid new-listing-card">
                    <div className="row listing-admin-area">
                        <div className="col-12">
                            <button type="button"
                                    className="btn btn-sm btn-outline-info mr-1">
                                {listing.address}
                            </button>
                            <a href={lease.detail_link}
                               target="_blank"
                               className="btn btn-sm btn-outline-info mr-1">Manage
                            </a>
                            <a href={listing.listing_link}
                               target="_blank"
                               className="btn btn-sm btn-outline-info mr-1">Listing
                            </a>
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
                            <div className="row listing-area-data-row">
                                <div className="col-sm-4 text-left">
                                    <b>Address</b>
                                </div>
                                <div className="col-sm-8 text-left">
                                    {listing.address}
                                </div>
                            </div>
                            {lease.leasemember_set.map(member =>
                            <div key={`${member.short_id}`}  className="row listing-area-data-row">
                                <div className="col-sm-4 text-left">
                                    <b>Client Name</b>
                                </div>
                                <div className="col-sm-8 text-left">
                                    {member.name}
                                </div>
                            </div>)}
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
                                    <b>Description</b>
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
                                    <b>Created By</b>
                                </div>
                                <div className="col-sm-8 text-left">
                                    {creator && creator.first_name} {creator && creator.last_name}
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

                            <div className="row">
                                <div className="listing-card-stub container-fluid">
                                    <table className="table">
                                        <tbody>
                                        <tr>
                                            <td style={{width: "90px"}}>
                                                <img
                                                    className="rounded-circle img-fluid mx-auto"
                                                    width="75"
                                                    height="75"
                                                    src={`${listing.listing_agent.avatar_url}`}
                                                    alt="Missing"/>
                                                </td>
                                            <td>
                                                <div className="mb-2">
                                                    <strong>{
                                                        listing
                                                        .listing_agent.get_full_name
                                                    }</strong> ·
                                                    Listing Agent
                                                </div>
                                                <div>Contact: {
                                                    listing
                                                    .listing_agent.phone
                                                }</div>
                                                <div>{
                                                    listing
                                                    .listing_agent.email
                                                }</div>
                                            </td>
                                        </tr>
                                        <tr>
                                            <td style={{width: "90px"}}>
                                                <img
                                                    className="rounded-circle img-fluid mx-auto"
                                                    width="75"
                                                    height="75"
                                                    src={`${listing.sales_agent.avatar_url}`}
                                                    alt="Missing"/>
                                            </td>
                                            <td>
                                                <div className="mb-2">
                                                    <strong>{
                                                        listing
                                                        .sales_agent.get_full_name
                                                    }</strong> ·
                                                    Sales Agent
                                                </div>
                                                <div>Contact: {
                                                    listing
                                                    .sales_agent.phone
                                                }</div>
                                                <div>{
                                                    listing
                                                    .sales_agent.email
                                                }</div>
                                            </td>
                                        </tr>
                                        </tbody>
                                    </table>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
}
