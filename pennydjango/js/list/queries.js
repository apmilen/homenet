import gql from 'graphql-tag'

export const GET_ALL_RENT_PROPERTIES = gql`
allRentProperty {
    id: pk
    latitude
    longitude
    address
    about
    contact
    price
}`

export const GET_RENT_PROPERTY = ({id}) => gql`
rentProperty(id: "${id}") {
    id: pk
    latitude
    longitude
    address
    about
    contact
    price
}`
