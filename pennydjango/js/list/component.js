import React, {Component} from 'react'

import {Query, Mutation} from 'react-apollo'
import {GET_RENTP} from '@/list/queries'
import {CREATE_RENTP} from '@/list/mutations'


class CreateRentProperty extends Component {
    constructor(props) {
        super(props)
        this.state = {
            price: 0,
            contact: '',
            address: '',
            latitude: 1,
            longitude: -1,
            about: '',
            bedrooms: 0,
            baths: 0,
            pets_allowed: true,
            amenities: ''
        }
    }
    render() {
        const { 
            price,
            contact,
            address,
            latitude,
            longitude,
            about,
            bedrooms,
            baths,
            pets_allowed,
            amenities,
        } = this.state

        const input = {
            rentproperty: {
                price,
                contact,
                address,
                latitude,
                longitude,
                about,
                bedrooms,
                baths,
                petsAllowed: pets_allowed,
                amenities,
            }
        }

        return <div>
            <div className="flex flex-column mt3">
                <input className="mb2" value={price}
                    onChange={e => this.setState({ price: e.target.value })}
                    type="number" placeholder="Price"
                />
                <input className="mb2" value={contact}
                    onChange={e => this.setState({ contact: e.target.value })}
                    type="text" placeholder="Contact"
                />
                <input className="mb2" value={address}
                    onChange={e => this.setState({ address: e.target.value })}
                    type="text" placeholder="Address"
                />
                <input className="mb2" value={latitude}
                    onChange={e => this.setState({ latitude: e.target.value })}
                    type="number" placeholder="Latitude"
                />
                <input className="mb2" value={longitude}
                    onChange={e => this.setState({ longitude: e.target.value })}
                    type="number" placeholder="Longitude"
                />
                <input className="mb2" value={about}
                    onChange={e => this.setState({ about: e.target.value })}
                    type="text" placeholder="About"
                />
                <input className="mb2" value={bedrooms}
                    onChange={e => this.setState({ bedrooms: e.target.value })}
                    type="number" placeholder="Bedrooms"
                />
                <input className="mb2" value={baths}
                    onChange={e => this.setState({ baths: e.target.value })}
                    type="number" placeholder="Baths"
                />
                <input className="mb2" value={pets_allowed}
                    onChange={e => this.setState({ pets_allowed: e.target.value })}
                    type="checkbox" placeholder="Pets allowed"
                />
                <input className="mb2" value={amenities}
                    onChange={e => this.setState({ amenities: e.target.value })}
                    type="text" placeholder="Amenities"
                />
            </div>

            <Mutation mutation={CREATE_RENTP} variables={{ input }}>
                {(createRentp, {data, error}) => {
                    if (data) console.log("LA DATA", data)
                    if (error) console.log("LE ERROR", error)

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