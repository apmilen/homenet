import gql from 'graphql-tag'

export const GET_RENTP = gql`
  {
    allRentp{
        id
        latitude
        longitude
        about
        contact
  }
}
`