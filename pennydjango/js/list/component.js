import React from 'react'

import {Query} from 'react-apollo'
import {GET_RENTPROPERTIES} from '@/list/queries'



const RentPropertyListItem = ({pk, price, contact, about, longitude, latitude, address}) =>
    <div>
        <ul key={pk} style={{display: 'inline-block', verticalAlign: 'top', marginRight: 20}}>
            <li>{price}</li>
            <li>{contact}</li>
            <li>{about}</li>
            <li>{longitude}</li>
            <li>{latitude}</li>
            <li>{address}</li>
        </ul>
        <iframe width="600" height="300" src={`https://maps.google.com/maps?q=${encodeURIComponent(address)}&t=&z=13&ie=UTF8&iwloc=&output=embed`} frameborder="0" scrolling="no" marginheight="0" marginwidth="0" style={{display: 'inline-block'}}></iframe>
    </div>


export const RentPropertyList = () =>
    <Query query={GET_RENTPROPERTIES}>
        {({loading, error, data}) => {
            if (loading)
                return 'Loading...'

            if (error)
                return `Unfortunately, got an error! ${error.message}`

            console.log(data)

            return <div>
                {data.rentpropertys.edges.map(({node}) =>
                    <RentPropertyListItem {...node}/>)}
            </div>
        }}
    </Query>
