import React from 'react'
import ReactDOM from 'react-dom'

import {
    Row, Card, FormControl, Button, Alert
} from 'react-bootstrap'


class UserCard extends React.Component {
    render() {
        const user = this.props

        return (
            <Card style={{ width: '18rem', margin: 5 }}>
                <Card.Header as="h3">{user.first_name || 'Unnamed'}</Card.Header>
                <div style={{ padding: 20 }}>
                    <div class="circle-avatar" style={{ backgroundImage: `url(${user.avatar_url})` }}></div>
                </div>
                <Card.Body>
                    <Card.Title>@{user.username}</Card.Title>
                    <Card.Subtitle className="mb-2 text-muted">{user.email || 'no email'}</Card.Subtitle>
                    <Card.Subtitle className="mb-2 text-muted">{user.user_type_str}</Card.Subtitle>
                </Card.Body>
            </Card>
        )
    }
}


class Users extends React.Component {
    constructor(props) {
        super(props)
        this.state = {
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
        const {email, user_type} = this.state
        const post_data = {type: 'NEW_USER', email, user_type}

        $.post('', post_data, (resp) => {
            if (resp.success) {
                const new_users = this.state.users.concat(resp.new_user)
                this.setState({
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
            <div>
                <Row className="justify-content-center" style={{ padding: 10 }}>
                    {users.map(user =>
                        <UserCard {...user} />
                    )}
                    <Card style={{ width: '18rem', margin: 5 }}>
                        <div style={{ margin: 'auto', padding: '60px 0' }}>
                            {this.state.errors &&
                                <Alert variant='danger' style={{textAlign: 'center', maxWidth: '13rem'}}>
                                    {this.state.errors}
                                </Alert>
                            }
                            <FormControl id='email'
                                         type='email'
                                         value={this.state.email}
                                         placeholder='Enter email'
                                         onChange={::this.changeField} />
                            <br/>
                            <FormControl id='user_type'
                                         as='select'
                                         value={this.state.user_type}
                                         onChange={::this.changeField} >
                                {user_types.map(user_type =>
                                    <option value={user_type[0]}>{user_type[1]}</option>
                                )}
                            </FormControl>
                            <br/>
                            <Button variant="primary" onClick={::this.postUser}>
                                Send invitation
                            </Button>

                        </div>
                    </Card>
                </Row>
            </div>
        )
    }
}


ReactDOM.render(
    React.createElement(Users, global.props),
    global.react_mount,
)
