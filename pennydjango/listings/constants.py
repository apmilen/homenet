# Listing Types
APARTMENT_TYPE = 'apartment'
HOUSE_TYPE = 'house'
COMMERCIAL = 'commercial'
LISTING_TYPES = (
    (APARTMENT_TYPE, 'Apartment'),
    (HOUSE_TYPE, 'House'),
    (COMMERCIAL, 'Commercial'),
)

# Listing Status
DRAFT = 'draft'
APPROVED = 'approved'
CANCELLED = 'cancelled'
RENTED = 'rented'
LISTING_STATUS = (
    (DRAFT, 'Draft'),
    (APPROVED, 'Approved'),
    (CANCELLED, 'Cancelled'),
    (RENTED, 'Rented')
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

# Parking Options
PARKING_OPTIONS = [
    ('dedicated_reserved_spot', 'Dedicated reserved spot'),
    ('shared_street_permit_parking', 'Shared street permit parking'),
    ('shared_public_street_parking', 'Shared public street parking'),
    ('no_parking_available', 'No parking available'),
]

# Transit options
TRANSIT_OPTIONS = (
    ('dyre_avenue_line', 'Dyre Avenue Line (Bronx) 5'),
    ('jerome_avenue_line', 'Jerome Avenue Line (Bronx) 4 5'),
    ('pelham_line', 'Pelham Line (Bronx) 6'),
    ('white_plains_road_line', 'White Plains Road Line (Bronx) 2 5'),
    ('concourse_line', 'Concourse Line (Bronx Manhattan) B D'),
    ('broadway_seventh_avenue', 'Broadway–Seventh Avenue Line (Bronx Manhattan Brooklyn) 1 2 3'),
    ('fourth_avenue_line', 'Fourth Avenue Line (Brooklyn) D N R W'),
    ('brighton_line', 'Brighton Line (Brooklyn) B Q'),
    ('culver_line', 'Culver Line (Brooklyn) F G'),
    ('eastern_parkway_line', 'Eastern Parkway Line (Brooklyn) 2 3 4 5'),
    ('franklin_avenue_line', 'Franklin Avenue Line (Brooklyn) S'),
    ('new_lots_line', 'New Lots Line Line (Brooklyn) 2 3 4 5'),
    ('nostrand_avenue_line', 'Nostrand Avenue Line Line (Brooklyn) 2 5'),
    ('sea_beach_line', 'Sea Beach Line (Brooklyn) N W'),
    ('west_end_line', 'West End Line (Brooklyn) D'),
    ('crosstown_line', 'Crosstown Line (Brooklyn Queens) G'),
    ('fulton_street_line', 'Fulton Street Line (Brooklyn Queens) A C'),
    ('jamaica_line', 'Jamaica Line (Brooklyn Queens) J M Z'),
    ('myrtle_avenue_line', 'Myrtle Avenue Line (Brooklyn Queens) M'),
    ('second_avenue_line', 'Second Avenue Line (Manhattan) N Q R'),
    ('42nd_street_shuttle', '42nd Street Shuttle (Manhattan) S'),
    ('63rd_street_line', '63rd Street Line (Manhattan) N Q R'),
    ('broadway_line', 'Broadway Line (Manhattan) N Q R W'),
    ('lenox_avenue_line', 'Lenox Avenue Line (Manhattan) 2 3'),
    ('lexington_avenue_line', 'Lexington Avenue Line (Manhattan) 5 4 6'),
    ('nassau_street_line', 'Nassau Street Line (Manhattan) K M Z'),
    ('sixth_avenue_line', 'Sixth Avenue Line (Manhattan Brooklyn) B D F M'),
    ('eighth_avenue_line', 'Eighth Avenue Line (Manhattan Brooklyn) A B C D E'),
    ('canarsie_line', 'Canarsie Line (Manhattan Brooklyn) L'),
    ('63rd_street_line', '63rd Street Line (Manhattan Queens) F'),
    ('flushing_line', 'Flushing Line (Manhattan Queens) 7'),
    ('queens_boulevard_line', 'Queens Boulevard Line (Manhattan Queens) E F M R'),
    ('archer_avenue_line', 'Archer Avenue Line (Queens) J Z'),
    ('archer_avenue_line_e', 'Archer Avenue Line E (Queens) E'),
    ('astoria_line', 'Astoria Line (Queens) N W'),
    ('rockaway_line', '	Rockaway Line (Queens) A S'),
)
