import React from 'react'
import ReactDOM from 'react-dom'
import { ApolloClient } from 'apollo-client'
import { HttpLink } from 'apollo-link-http'
import { InMemoryCache } from 'apollo-cache-inmemory'
import { ApolloProvider } from 'react-apollo'

import ListView from "@/list/component"


global.loading = global.loading || {end: Date.now()}
if (!global.history) {
    global.history = global.history || {pushState: () => {}}
}

export const Home = {
    view: 'ui.views.pages.Home',
    init(props) {
        const link = new HttpLink({
            uri: props.endpoint
        })
        const client = new ApolloClient({
          link: link,
          cache: new InMemoryCache(),
        })
        return {props, client}
    },
    render({client}) {
        return <ApolloProvider client={client}>
            <ListView/>
        </ApolloProvider>
    },
    mount(props, mount_point) {
        global.page = this.init(props)
        ReactDOM.render(
            this.render(global.page),
            mount_point,
        )
    },
}

if (global.react_mount) {
    // we're in a browser, so mount the page
    Home.mount(global.props, global.react_mount)
}
