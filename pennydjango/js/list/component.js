import React, {Component} from 'react'

import {Query, Mutation} from 'react-apollo'
import {GET_USERS, GET_RENTPROPERTIES} from '@/list/queries'
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



const RentPropertyListItem = ({pk, price, contact, about, longitude, latitude, address, amenities, bedrooms, baths, petsAllowed, publisher}) =>
    <div class="col-md-4 rental-list-item">
        <div class="list-item-content">
            <h3>{about}</h3>
            <div><b>Price:</b> ${price}/month</div>
            <div><b>Size:</b> {bedrooms} bedrooms, {baths} bathrooms</div>
            <div><b>Amenities:</b> {amenities}</div>
            <div><b>Pets Allowed:</b> {petsAllowed ? '😸 yes' : '😿 no'}</div>
            <div><b>Primary Contact:</b> {contact}</div>
        </div>
        <br/>
        <h4>{address} ({latitude}, {longitude})</h4>
        <iframe src={`https://maps.google.com/maps?q=${encodeURIComponent(address)}&t=&z=13&ie=UTF8&iwloc=&output=embed`} frameborder="0" scrolling="no" marginheight="0" marginwidth="0" style={{display: 'inline-block'}}></iframe>
    </div>


export const RentPropertyList = () =>
    <Query query={GET_RENTPROPERTIES}>
        {({loading, error, data}) => {
            if (loading)
                return 'Loading...'

            if (error)
                return `Got an error! ${error.message}`

            // console.log(data)

            return <div>
                {data.rentpropertys.edges.map(({node}) =>
                    <RentPropertyListItem {...node}/>)}
            </div>
        }}
    </Query>



const UserListItem = ({pk, username, email, name}) =>
    <div class="user-list-item">
        <div><b>Username:</b> {username}</div>
        <div><b>Email:</b> {email}</div>
        <div><b>Name:</b> {name}</div>
    </div>

export const UserList = () =>
    <Query query={GET_USERS}>
        {({loading, error, data}) => {
            if (loading)
                return 'Loading...'

            if (error)
                return `Got an error! ${error.message}`

            // console.log(data)

            return <div>
                {data.users.edges.map(({node}) =>
                    <UserListItem {...node}/>)}
            </div>
        }}
    </Query>
