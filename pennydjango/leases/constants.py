DEFAULT_LEASE_STATUS = 'unsigned_unapproved'
LEASE_STATUS = (
    (DEFAULT_LEASE_STATUS, 'Unsigned, Unapproved'),
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
