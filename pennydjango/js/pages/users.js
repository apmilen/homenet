import React from 'react'
import ReactDOM from 'react-dom'

import {
    Row, Card, FormControl, Alert, InputGroup, Badge
} from 'react-bootstrap'
import {
    Modal, ModalBody, ModalHeader, ModalFooter, Button, FormCheckbox
} from 'shards-react'

import {FiltersBar} from '@/components/filtersbar'
import {SettingsGear} from '@/components/misc'


class UserModal extends React.Component {
    constructor(props) {
        super(props)
        this.state = {
            open: false,
            ...props.user
        }
    }
    toggle() {
        this.setState({open: !this.state.open, ...this.props.user})
    }
    changeField(e) {
        this.setState({[e.target.id]: e.target.value})
    }
    toggleField(e) {
        this.setState({[e.target.id]: !this.state[e.target.id]})
    }
    updateUser() {
        const {
            id, first_name, last_name, email, is_active, user_type
        } = this.state
        this.props.updateUser({
            id, first_name, last_name, email, is_active, user_type
        })
        this.toggle()
    }
    render() {
        const {
            open, first_name, last_name, email, is_active, user_type
        } = this.state
        const {constants} = global.props

        return (
            <div className="usercard-modal">
                <SettingsGear onClick={::this.toggle}/>
                <Modal open={open} toggle={::this.toggle}>
                    <ModalHeader>Modify user</ModalHeader>
                    <ModalBody>
                        <h6>⚠️ Warning: update this info at your own risk</h6>
                        <div>
                            <FormControl id='first_name' className="my-2" type='text'
                                         value={first_name} placeholder='First name'
                                         autoComplete="off"
                                         onChange={::this.changeField} />
                            <FormControl id='last_name' className="my-2" type='text'
                                         value={last_name} placeholder='Last name'
                                         autoComplete="off"
                                         onChange={::this.changeField} />
                            <FormControl id='email' className="my-2"
                                         type='email'
                                         value={email}
                                         placeholder='User email'
                                         autoComplete="off"
                                         onChange={::this.changeField} />
                            <FormControl id='user_type' className="my-2"
                                         as='select'
                                         value={user_type}
                                         onChange={::this.changeField} >
                                {Object.keys(constants.user_type).map(u_type =>
                                    <option key={u_type} value={u_type}>{constants.user_type[u_type]}</option>
                                )}
                            </FormControl>
                            <FormCheckbox id='is_active'
                                          checked={is_active}
                                          onChange={::this.toggleField}>
                                is active
                            </FormCheckbox>
                        </div>
                    </ModalBody>
                    <ModalFooter>
                        <Button outline theme="secondary" onClick={::this.toggle}>Cancel</Button>
                        <Button theme="warning" onClick={::this.updateUser}>Update</Button>
                    </ModalFooter>
                </Modal>
            </div>
        )
    }
}

class UserCard extends React.Component {
    render() {
        const {user, updateUser} = this.props
        const user_variant = {
            admin: "primary",
            agent: "secondary",
            client: "info",
        }

        return (
            <Card style={{ width: '18rem', height: 370, margin: 5 }}>
                <UserModal user={user} updateUser={updateUser}/>
                <Badge variant={user_variant[user.user_type]}
                       className="usercard-badge">
                    {user.user_type_str}
                </Badge>
                {!user.is_active &&
                    <Badge variant="danger" className="usercard-inactive-badge">
                        INACTIVE
                    </Badge>
                }
                <div style={{ padding: '20px 0', margin: '0 30px' }}>
                    <a href={user.profile_link} target="_blank">
                        <div className="circle-avatar" style={{ backgroundImage: `url(${user.avatar_url})` }}></div>
                    </a>
                </div>
                <div style={{ padding: '0 1.9rem' }}>
                    <h3>{user.first_name || 'Unnamed'}</h3>
                    <Card.Title className="text-muted">{user.email || 'no email'}</Card.Title>
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
            email: '',
            user_type: "agent",
            users: [],
            errors: '',
        }
    }
    changeField(e) {
        this.setState({[e.target.id]: e.target.value})
    }
    postUser() {
        const {name, email, user_type} = this.state
        const post_data = {
            type: 'NEW_USER',
            name, email, user_type
        }

        $.post('', post_data, (resp) => {
            if (resp.success) {
                const new_users = [resp.new_user].concat(this.state.users)
                this.setState({
                    name: '',
                    email: '',
                    users: new_users,
                    errors: ''
                })
            } else {
                this.setState({errors: resp.details})
            }
        })
    }
    fetchUsers(params) {
        const post_data = {...params, type: 'FILTER_USER'}
        $.post('', post_data, (resp) =>
            this.setState({users: resp.users})
        )
    }
    updateUser(params) {
        const post_data = {...params, type: 'UPDATE_USER'}
        $.post('', post_data, (resp) => {
            const users_without_user = this.state.users.filter(user => user.id != resp.user.id)
            this.setState({users: [resp.user].concat(users_without_user)})
        })
    }
    render() {
        const {constants} = this.props
        const {users} = this.state
        const filters = ["searching_text", "only_active", "user_type"]

        return <>
            <FiltersBar filters={filters}
                        constants={constants}
                        updateParams={::this.fetchUsers} />
            <Row className="justify-content-center usercards-container">
                <Card style={{ width: '18rem', height: 370, margin: 5 }}>
                    <div style={{ margin: 'auto', width: '80%' }}>
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
                        <FormControl id='email' className="my-2"
                                     type='email'
                                     value={this.state.email}
                                     placeholder='Enter email'
                                     onChange={::this.changeField} />
                        <FormControl id='user_type' className="my-2"
                                     as='select'
                                     value={this.state.user_type}
                                     onChange={::this.changeField} >
                            {Object.keys(constants.user_type).map(u_type =>
                                <option key={u_type} value={u_type}>{constants.user_type[u_type]}</option>
                            )}
                        </FormControl>
                        <Button onClick={::this.postUser}>
                            Send invitation
                        </Button>

                    </div>
                </Card>
                {users.map(user =>
                    <UserCard key={user.id} user={user} updateUser={::this.updateUser} />
                )}
            </Row>
        </>
    }
}


ReactDOM.render(
    React.createElement(Users, global.props),
    global.react_mount,
)
