import gql from 'graphql-tag'

export const GET_ALL_RENT_PROPERTIES = gql`
query allRentProperty {
    rentpropertys {
        id: pk
        latitude
        longitude
        address
        about
        contact
        price
        created
        modified
        publisher {
            id: pk
            username
        }
    }
}`

export const GET_RENT_PROPERTY = ({id}) => gql`
query rentProperty($id: UUID!) {
    rentproperty(id: $id) {
        id: pk
        latitude
        longitude
        address
        about
        contact
        price
        created
        modified
        publisher {
            id: pk
            username
        }
    }
}`
