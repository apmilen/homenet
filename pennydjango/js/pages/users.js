import React from 'react'
import ReactDOM from 'react-dom'

import {
    Row, Card, Button
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
    render() {
        const {users} = this.props
        return (
            <div>
                <Row className="justify-content-center" style={{ padding: 10 }}>
                    {users.map(user =>
                        <UserCard {...user} />
                    )}
                    <Card style={{ width: '18rem', margin: 5 }} className="overlay-parent">
                        <a href="new/" className="overlay"></a>
                        <i style={{ fontSize: '12rem', margin: 'auto' }}
                           class="material-icons">add_circle_outline</i>
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
