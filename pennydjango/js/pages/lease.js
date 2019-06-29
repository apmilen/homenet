import React from 'react'
import ReactDOM from 'react-dom'

import {Lease} from '@/leases/components'

export const LeasePage = (props) => {
    return <Lease key={props.lease.short_id} lease={props.lease}/>
}

ReactDOM.render(
    React.createElement(LeasePage, global.props),
    global.react_mount,
)