import React from 'react'

import {Query} from 'react-apollo'
import {GET_USERS, GET_RENTPROPERTIES} from '@/list/queries'



const RentPropertyListItem = ({pk, price, contact, about, longitude, latitude, address, amenities, bedrooms, baths, petsAllowed, publisher}) =>
    <div class="col-md-3">
        <div class="rental-list-item">
            <div class="list-item-content">
                <h3>{about}</h3>
                <hr/>
                <div><b>Price:</b> ${price}/month</div>
                <div><b>Size:</b> {bedrooms} bedrooms, {baths} bathrooms</div>
                <div><b>Amenities:</b> {amenities}</div>
                <div><b>Pets Allowed:</b> {petsAllowed ? '😸 yes' : '😿 no'}</div>
                <div><b>Primary Contact:</b> {contact}</div>
                <div><b>Listing Owner:</b> {publisher.username} ({publisher.email})</div>
            </div>
            <br/>
            <h4>{address} ({latitude}, {longitude})</h4>
            <iframe src={`https://maps.google.com/maps?q=${encodeURIComponent(address)}&t=&z=13&ie=UTF8&iwloc=&output=embed`} frameborder="0" scrolling="no" marginheight="0" marginwidth="0" style={{display: 'inline-block'}}></iframe>
        </div>
    </div>


export const RentPropertyList = () =>
    <Query query={GET_RENTPROPERTIES}>
        {({loading, error, data}) => {
            if (loading)
                return 'Loading...'

            if (error)
                return `Got an error! ${error.message}`

            // console.log(data)

            return <div class="row" style={{backgroundColor: 'rgba(225, 255, 225, 0.66)', padding: 20}}>
                {data.rentpropertys.edges.map(({node}) =>
                    <RentPropertyListItem {...node}/>)}
            </div>
        }}
    </Query>


const UserListItem = ({pk, username, email, name}) =>
    <div class="col-md-3 user-list-item">
        <div><b>Username:</b> {username}</div>
        <div><b>Email:</b> {email}</div>
        <div><b>Name:</b> {name}</div>
    </div>

export const UserList = () =>
    <Query query={GET_USERS}>
        {({loading, error, data}) => {
            if (loading)
                return 'Loading...'

            if (error)
                return `Got an error! ${error.message}`

            // console.log(data)

            return <div class="row">
                {data.users.edges.map(({node}) =>
                    <UserListItem {...node}/>)}
            </div>
        }}
    </Query>
