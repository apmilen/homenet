import React from 'react'
import ReactDOM from 'react-dom'
import { ApolloClient } from 'apollo-client'
import { ApolloLink } from 'apollo-link'
import { HttpLink } from 'apollo-link-http'
// import { RetryLink } from 'apollo-link-retry'
import { onError } from 'apollo-link-error'
import { InMemoryCache } from 'apollo-cache-inmemory'
import { ApolloProvider } from 'react-apollo'

import {RentalPropertyListView} from "@/list/component"


global.loading = global.loading || {end: Date.now()}
if (!global.history) {
    global.history = global.history || {pushState: () => {}}
}

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

export const Home = {
    view: 'ui.views.pages.Home',
    init(props) {
        const ErrorHandledLink = onError(({graphQLErrors, networkError}) => {
            // if (graphQLErrors) {
            //     for (const {message, locations, path} of graphQLErrors) {
            //         console.log(`[GraphQL error]: Message: ${message}, Location: ${locations}, Path: ${path}`)
            //     }
            // }
            // if (networkError) {
            //     console.log(`[Network error]: ${networkError}`)
            // }
        })
        const link = ApolloLink.from([
            // new RetryLink(),
            ErrorHandledLink,
            new HttpLink({
                uri: props.endpoint,
                // fetchOptions: {mode: 'no-cors'},
                // credentials: "same-origin",
                headers: {
                    "X-CSRFToken": getCookie("csrftoken"),
                },
            })
        ])
        const client = new ApolloClient({
            link: link,
            cache: new InMemoryCache(),
            onError: (e) => {console.log(e)},
        })
        return {props, client}
    },
    render({client}) {
        return <ApolloProvider client={client}>
            <RentalPropertyListView/>
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
