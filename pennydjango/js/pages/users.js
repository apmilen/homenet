import React from 'react'
import ReactDOM from 'react-dom'

import {
    Row, Card, FormControl, Button, Alert, InputGroup
} from 'react-bootstrap'


class UserCard extends React.Component {
    render() {
        const user = this.props

        return (
            <Card style={{ width: '18rem', height: 370, margin: 5 }}>
                <div style={{ padding: '20px 0', margin: '0 30px' }}>
                    <div class="circle-avatar" style={{ backgroundImage: `url(${user.avatar_url})` }}></div>
                </div>
                <div style={{ padding: '0 1.9rem' }}>
                <h3>{user.first_name || 'Unnamed'}</h3>
                <Card.Title>@{user.username}</Card.Title>
                <Card.Subtitle className="text-muted">{user.email || 'no email'}</Card.Subtitle>
                <Card.Subtitle className="">{user.user_type_str}</Card.Subtitle>
                </div>
            </Card>
        )
    }
}


class Users extends React.Component {
    constructor(props) {
        super(props)
        this.state = {
            name: '',
            username: '',
            email: '',
            user_type: props.user_types[0][0],
            users: props.users,
            errors: '',
        }
    }
    changeField(e) {
        this.setState({[e.target.id]: e.target.value})
    }
    postUser() {
        const {name, username, email, user_type} = this.state
        const post_data = {
            type: 'NEW_USER',
            name, username, email, user_type
        }

        $.post('', post_data, (resp) => {
            if (resp.success) {
                const new_users = this.state.users.concat(resp.new_user)
                this.setState({
                    name: '',
                    username: '',
                    email: '',
                    users: new_users,
                    errors: ''
                })
            } else {
                this.setState({errors: resp.details})
            }
        })
    }
    render() {
        const {user_types} = this.props
        const {users} = this.state

        return (
            <Row className="justify-content-center usercards-container">
                <Card style={{ width: '18rem', height: 370, margin: 5 }}>
                    <div style={{ margin: 'auto', padding: '60px 0', width: '80%' }}>
                        {this.state.errors &&
                            <Alert variant='danger' style={{textAlign: 'center', width: '100%'}}>
                                {this.state.errors}
                            </Alert>
                        }
                        <h4>Add person:</h4>
                        <FormControl id='name' className="my-2"
                                     type='text'
                                     value={this.state.name}
                                     placeholder='Name'
                                     onChange={::this.changeField} />
                        <InputGroup className="my-2">
                            <InputGroup.Prepend>
                                <InputGroup.Text>@</InputGroup.Text>
                            </InputGroup.Prepend>
                            <FormControl id='username'
                                         type='text'
                                         value={this.state.username}
                                         placeholder='username'
                                         onChange={::this.changeField} />
                        </InputGroup>
                        <FormControl id='email' className="my-2"
                                     type='email'
                                     value={this.state.email}
                                     placeholder='Enter email'
                                     onChange={::this.changeField} />
                        <FormControl id='user_type' className="my-2"
                                     as='select'
                                     value={this.state.user_type}
                                     onChange={::this.changeField} >
                            {user_types.map(user_type =>
                                <option value={user_type[0]}>{user_type[1]}</option>
                            )}
                        </FormControl>
                        <Button variant="primary" onClick={::this.postUser}>
                            Send invitation
                        </Button>

                    </div>
                </Card>
                {users.map(user =>
                    <UserCard {...user} />
                )}
            </Row>
        )
    }
}


ReactDOM.render(
    React.createElement(Users, global.props),
    global.react_mount,
)
