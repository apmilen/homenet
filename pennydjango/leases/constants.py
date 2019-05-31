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
