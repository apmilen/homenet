import React from 'react'

import {Query} from 'react-apollo'
import {GET_RENT_PROPERTIES} from '@/list/queries'


export const RentalPropertyListView = () =>
    <Query query={GET_RENT_PROPERTIES} variables={{price__gt: 0}}>
        {({loading, error, data}) => {
            console.log(error)
            if (loading)
                return 'Loading...'

            if (error)
                return `Unfortunately, got an error! ${error.message}`


            return <div>
                {/*data.allRentProperty.map(rentp =>
                    <div>
                        <ul key={rentp.pk} style={{display: 'inline-block', verticalAlign: 'top', marginRight: 20}}>
                            <li>{rentp.price}</li>
                            <li>{rentp.contact}</li>
                            <li>{rentp.about}</li>
                            <li>{rentp.longitude}</li>
                            <li>{rentp.latitude}</li>
                            <li>{rentp.address}</li>
                        </ul>
                        <iframe width="600" height="300" src={`https://maps.google.com/maps?q=${encodeURIComponent(rentp.node.address)}&t=&z=13&ie=UTF8&iwloc=&output=embed`} frameborder="0" scrolling="no" marginheight="0" marginwidth="0" style={{display: 'inline-block'}}></iframe>
                    </div>
                )*/}
            </div>
        }}
    </Query>
