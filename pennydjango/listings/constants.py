# Listing Types
APARTMENT_TYPE = 'apartment'
HOUSE_TYPE = 'house'
LISTING_TYPES = (
    (APARTMENT_TYPE, 'Apartment'),
    (HOUSE_TYPE, 'House')
)

# Listing Status
DRAFT = 'draft'
APPROVED = 'approved'
NON_APPROVED = 'not_approved'
LISTING_STATUS = (
    (DRAFT, 'Draft'),
    (APPROVED, 'Approved'),
    (NON_APPROVED, 'Not Approved')
)


# Move in cost types
MOVE_IN_COST = (
    ('first_last_security', 'First, Last, and Security'),
    ('first_security', 'First and Security')
)


# Pets allowed types
PETS_ALLOWED = (
    ('all', 'All Pets Allowed'),
    ('upon_approval', 'Pets Upon Approval'),
    ('dogs', 'Dogs Allowed'),
    ('small_dogs', 'Small Dogs Allowed'),
    ('cats', 'Cats Allowed'),
    ('small_pets', 'Small Pets Allowed'),
    ('no_pets', 'No pets allowed')
)

# Amenities (Listing Detail)

# Basics
BASICS = (
    ('central_ac', 'Central A/C'),
    ('doorman', 'Doorman'),
    ('exposed_brick', 'Exposed Brick'),
    ('high_ceilings', 'High Ceilings'),
    ('hardwood_floors', 'Hardwood Floors'),
    ('video_intercom', 'Video Intercom'),
    ('elevator', 'Elevator'),
    ('furnished', 'Furnished'),
    ('natural_light_la', 'Natural Light in Living Area'),
    ('washer_dryer_installed', 'Washer Dryer Installed'),
    ('washer_dryer_hookup', 'Washer Dryer Hookup'),
    ('laundry_in_building', 'Laundry in Building'),
    ('waterfront_view_fu', 'Waterfront View from Unit'),
)

# Building
BUILDING = (
    ('bike_storage', 'Bike Storage'),
    ('storage_space', 'Storage Space'),
    ('gym', 'Gym'),
    ('wheelchair_accessible', 'Wheelchair Accessible'),
    ('game_room', 'Game Room'),
    ('screening_room', 'Screening Room'),
    ('lounge', 'Lounge'),
    ('private_parking', 'Private Parking'),
    ('zipcar', 'Zipcar'),
    ('waterfront_view_from_roof', 'Waterfront View From Roof'),
    ('office_space', 'Office Space'),
    ('shared_workspace', 'Shared Workspace'),
    ('public_wifi', 'Public Wifi'),
)

# Outdoors
OUTDOORS = (
    ('outdoor_space', 'Outdoor Space'),
    ('common_courtyard', 'Common Courtyard'),
    ('private_backyard', 'Private Backyard'),
    ('shared_backyard', 'Shared Backyard'),
    ('balcony', 'Balcony'),
    ('terrace', 'Terrace'),
    ('patio', 'Patio'),
    ('roof_access', 'Roof Access'),
    ('private_roof_deck', 'Private Roof Deck'),
    ('skyline_view', 'Skyline View'),
)

# Kitchen
KITCHEN = (
    ('eat_in_kitchen', 'Eat in Kitchen'),
    ('stainless_steel_appliances', 'Stainless Steel Appliances'),
    ('dishwasher', 'Dishwasher'),
    ('built_in_microwave', 'Built in Microwave'),
    ('stone_countertops', 'Stone Countertops'),
    ('granite_countertops', 'Granite Countertops'),
)

# Luxury
LUXURY = (
    ('duplex', 'Duplex'),
    ('children_playroom', 'Children Playroom'),
    ('concierge', 'Concierge'),
    ('playground', 'Playground'),
    ('spa_services', 'Spa Services'),
    ('basement', 'Basement'),
)

# Sports
SPORTS = (
    ('swimming_pool', 'Swimming Pool'),
    ('tennis_courts', 'Tennis Courts'),
    ('volleyball_courts', 'Volleyball Courts'),
    ('basketball_courts', 'Basketball Courts'),
)

# Groups
AMENITIES = (
    ("Basics", BASICS),
    ("Building", BUILDING),
    ("Outdoors", OUTDOORS),
    ("Kitchen", KITCHEN),
    ("Luxury", LUXURY),
    ("Sports", SPORTS)
)
