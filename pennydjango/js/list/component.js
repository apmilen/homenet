import React from 'react'

import {Query} from 'react-apollo'
import {GET_RENTP} from '@/list/queries'

const Properties = () =>
    <Query query={GET_RENTP}>
        {({loading, error, data}) => {
            if (loading) return 'Loading...'
            if (error) return `Unfortunately, got an error! ${error.message}`

            return <div>
                {data.allRentp.edges.map(rentp =>
                    <div>
                        <ul key={rentp.node.modelId} style={{display: 'inline-block', verticalAlign: 'top', marginRight: 20}}>
                            <li>{rentp.node.price}</li>
                            <li>{rentp.node.contact}</li>
                            <li>{rentp.node.about}</li>
                            <li>{rentp.node.longitude}</li>
                            <li>{rentp.node.latitude}</li>
                            <li>{rentp.node.address}</li>
                        </ul>
                        <iframe width="600" height="300" src={`https://maps.google.com/maps?q=${encodeURIComponent(rentp.node.address)}&t=&z=13&ie=UTF8&iwloc=&output=embed`} frameborder="0" scrolling="no" marginheight="0" marginwidth="0" style={{display: 'inline-block'}}></iframe>
                    </div>
                )}
            </div>
        }}
    </Query>

export default class ListView extends React.Component {
    render() {
        return <Properties/>
    }
}
