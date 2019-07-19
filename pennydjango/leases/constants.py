DEFAULT_LEASE_STATUS = 'awaiting_deposit'
LEASE_STATUS = (
    (DEFAULT_LEASE_STATUS, 'Awaiting Deposit'),
    ('unsigned_unapproved', 'Unsigned, Unapproved'),
    ('unsigned_approved', 'Unsigned, Approved'),
    ('signed_approved', 'Signed, Approved'),
    ('client_backed_out', 'Client Backed Out'),
    ('cancelled', 'Cancelled'),
    ('awaiting_op', 'Awaiting OP'),
    ('pending_deletion', 'Pending Deletion')
)


APPLICANT_TYPE = (
    ('tenant', 'Tenant'),
    ('guarantor', 'Guarantor'),
    ('occupant', 'Occupant')
)


CHARGE_OPTIONS = [
    ('Bike Storage Fee', 'Bike Storage Fee'),
    ('Broker Fee', 'Broker Fee'),
    ('First Month Rent', 'First Month Rent'),
    ('Gym/Amenity Fee', 'Gym/Amenity Fee'),
    ('Last Month Rent', 'Last Month Rent'),
    ('Parking Spot Fee', 'Parking Spot Fee'),
    ('Pet Fee', 'Pet Fee'),
    ('Prepaid Rent', 'Prepaid Rent'),
    ('Security Deposit', 'Security Deposit'),
    ('Storage Fee', 'Storage Fee'),
    ('Utility Fee', 'Utility Fee'),
]


LEASE_STATUS_PROGRESS = {
    'client_backed_out': 0,
    'cancelled': 0,
    'pending_deletion': 0,
    'awaiting_deposit': 25,
    'unsigned_unapproved': 50,
    'unsigned_approved': 75,
    'signed_approved': 100,
    'awaiting_op': 100
}
