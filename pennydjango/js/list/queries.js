import gql from 'graphql-tag'

export const GET_RENTP = gql`
{
    allRentp {
        edges {
            node {
                modelId
                latitude
                longitude
                about
                contact
                price
            }
        }
    }
}`