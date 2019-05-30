import React from 'react'
import ReactDOM from 'react-dom'


class Listings extends React.Component {
    render() {
        return [
            <center><h1>AloHawaii</h1></center>
        ]
    }
}

ReactDOM.render(
    React.createElement(Listings, global.props),
    global.react_mount,
)
