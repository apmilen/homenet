
def get_short_uuid(uuid) -> str:
    """get the first block of a 4-word UUID to use as a short identifier"""
    full_uuid = str(uuid)
    return full_uuid.split('-', 1)[0]
