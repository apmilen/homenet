import gql from 'graphql-tag'

export const CREATE_RENTP = gql`
    mutation createRentP($input: CreateRentPropertyMutationInput!){
        createRentproperty (input: $input) {
            status
            formErrors
            rentproperty {
                id
            }
        }
    }
`