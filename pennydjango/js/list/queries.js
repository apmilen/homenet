import gql from 'graphql-tag'

export const GET_USERS = gql`
query users {
    users {
        edges {
            node {
                id: pk
                username
                email
            }
        }
    }
}`

export const GET_USER = gql`
query user($username: String!) {
    user(username: $username) {
        edges {
            node {
                id: pk
                username
                email
            }
        }
    }
}`

export const GET_RENTPROPERTIES = gql`
query rentpropertys {
    rentpropertys {
        edges {
            node {
                id: pk
                latitude
                longitude
                address
                about
                contact
                price
                bedrooms
                baths
                amenities
                petsAllowed
                created
                modified
                publisher {
                    id: pk
                    username
                    email
                }
            }
        }
    }
}`

export const GET_RENTPROPERTY = gql`
query rentproperty($id: UUID!) {
    rentproperty(id: $id) {
        edges {
            node {
                id: pk
                latitude
                longitude
                address
                about
                contact
                price
                bedrooms
                baths
                pets_allowed
                amenities
                created
                modified
                publisher {
                    id: pk
                    username
                    email
                }
            }
        }
    }
}`
