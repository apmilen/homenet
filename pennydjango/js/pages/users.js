import React from 'react'
import ReactDOM from 'react-dom'

import {
    Row, Card, Button
} from 'react-bootstrap'


class UserCard extends React.Component {
    render() {
        const user = this.props

        return (
            <Card style={{ width: '14rem', margin: 5 }}>
                <Card.Img variant="top" src={user.avatar_url} />
                <Card.Body>
                <Card.Title>{user.first_name || 'Unnamed'}</Card.Title>
                <Card.Subtitle className="mb-2 text-muted">@{user.username}</Card.Subtitle>
                <Card.Text>
                    Some quick example text
                </Card.Text>
                    <Button variant="primary">Go somewhere</Button>
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
                </Row>
            </div>
        )
    }
}

ReactDOM.render(
    React.createElement(Users, global.props),
    global.react_mount,
)
