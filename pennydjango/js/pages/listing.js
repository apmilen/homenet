import React from 'react'
import ReactDOM from 'react-dom'

import {ListingComponent} from '@/listings/components'

export const ListingPage = (props) => {
    return <ListingComponent key={props.listing.short_id} listing={props.listing}/>
}

ReactDOM.render(
    React.createElement(ListingPage, global.props),
    global.react_mount,
)