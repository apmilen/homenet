import gql from 'graphql-tag'

export const GET_RENTP = gql`
{
    allRentp {
        edges {
            node {
                id
                latitude
                longitude
                about
                contact
            }
        }
    }
}`