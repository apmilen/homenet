import React, {Component} from 'react'

import {Query, Mutation} from 'react-apollo'
import {GET_RENTP} from '@/list/queries'
import {CREATE_RENTP} from '@/list/mutations'


class CreateRentProperty extends Component {
    constructor(props) {
        super(props)
        this.state = {
            price: null,
            contact: '',
            address: '',
            latitude: null,
            longitude: null,
            about: '',
            bedrooms: null,
            baths: null,
            petsAllowed: true,
            amenities: ''
        }
    }
    changeField(e){
        this.setState({ [e.target.name]: e.target.value })
    }
    fieldType(field){
        switch (field) {
            case 'price':
            case 'latitude':
            case 'longitude':
            case 'bedrooms':
            case 'baths':
                return "number"

            case 'petsAllowed':
                return "checkbox"
        }
        return "text"
    }
    fieldPlaceholder(field){
        return field
    }
    render() {

        const input = {
            rentproperty: this.state
        }

        return <div>
            <div className="">
                {Object.keys(this.state).map((field, idx) => {
                    return <span>
                        <input
                            className="rent-input" name={field} value={this.state[field]}
                            onChange={::this.changeField}
                            type={this.fieldType(field)}
                            placeholder={this.fieldPlaceholder(field)}
                        />
                        {idx % 2 != 0 && <br/>}
                    </span>
                })}
            </div>

            <Mutation mutation={CREATE_RENTP} variables={{ input }}>
                {(createRentp, {data}) => {
                    if (data) {
                        console.log(data)
                        /*if (data.createRentproperty.status == 200) {
                            this.cleanFields()
                        }*/
                    }
                    return <button onClick={createRentp}>Send</button>
                }}
            </Mutation>
        </div>
      }

}

const Properties = () =>
    <Query query={GET_RENTP}>
        {({loading, error, data}) => {
            if (loading) return 'Loading...'
            if (error) return `Error! ${error.message}`

            return <>
                {data.allRentp.edges.map(rentp =>
                    <ul key={rentp.node.modelId}>
                        <li>{rentp.node.price}</li>
                        <li>{rentp.node.contact}</li>
                        <li>{rentp.node.about}</li>
                        <li>{rentp.node.longitude}</li>
                        <li>{rentp.node.latitude}</li>
                    </ul>
                )}
            </>
            }
        }
    </Query>

export default class ListView extends React.Component {
    render() {
        return <span>
            <Properties />
            <CreateRentProperty />
        </span>
    }
}