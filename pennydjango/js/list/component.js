import React from 'react'

import {Query} from 'react-apollo'
import {GET_USERS, GET_RENTPROPERTIES} from '@/list/queries'



const RentPropertyListItem = ({pk, price, contact, about, longitude, latitude, address}) =>
    <div class="rental-list-item">
        <div><b>Price</b> {price}</div>
        <div><b>Primary</b>Contact: {contact}</div>
        <div><b>About</b> {about}</div>
        <div><b>Location</b> {address} ({latitude}, {longitude})</div>
        <iframe width="600" height="300" src={`https://maps.google.com/maps?q=${encodeURIComponent(address)}&t=&z=13&ie=UTF8&iwloc=&output=embed`} frameborder="0" scrolling="no" marginheight="0" marginwidth="0" style={{display: 'inline-block'}}></iframe>
    </div>


export const RentPropertyList = () =>
    <Query query={GET_RENTPROPERTIES}>
        {({loading, error, data}) => {
            if (loading)
                return 'Loading...'

            if (error)
                return `Got an error! ${error.message}`

            // console.log(data)

            return <div>
                {data.rentpropertys.edges.map(({node}) =>
                    <RentPropertyListItem {...node}/>)}
            </div>
        }}
    </Query>


const UserListItem = ({pk, username, email, name}) =>
    <div style={{textAlign: 'left'}}>
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

            return <div>
                {data.users.edges.map(({node}) =>
                    <UserListItem {...node}/>)}
            </div>
        }}
    </Query>
