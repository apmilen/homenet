import React from 'react'

import {Query} from 'react-apollo'
import {GET_RENTP} from '@/list/queries'

const Properties = () =>
    <Query query={GET_RENTP}>
        {({loading, error, data}) => {
            if (loading) return 'Loading...'
            if (error) return `Error! ${error.message}`

            return <>
                {data.allRentp.edges.map(rentp =>
                    <ul key={rentp.node.modelId}>
                        <li>{rentp.node.price}</li>
                        <li>{rentp.node.contact}</li>
                        <li>{rentp.node.about}</li>
                        <li>{rentp.node.longitude}</li>
                        <li>{rentp.node.latitude}</li>
                    </ul>
                )}
            </>
            }
        }
    </Query>

export default class ListView extends React.Component {
    render() {
        return <Properties/>
    }
}