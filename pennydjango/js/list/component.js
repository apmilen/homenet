import React from 'react'

import {Query} from 'react-apollo'
import {GET_RENTP} from '@/list/queries'

const Properties = () =>
    <Query query={GET_RENTP}>
        {({loading, error, data}) => {
            if (loading) return 'Loading...'
            if (error) return `Error! ${error.message}`

            return <>
                {data.allRentp.map(rentp =>
                    <ul key={rentp.id}>
                        <li>{rentp.contact}</li>
                        <li>{rentp.about}</li>
                        <li>{rentp.longitude}</li>
                        <li>{rentp.latitude}</li>
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