def arrayfield_keys_to_values(keys, choices):
    values = []
    for key, value in choices:
        if key in keys:
            values.append(value)
    return values


def create_column_defs_list(column_defs):
    column_defs_list = []
    for index, column_def in enumerate(column_defs):
        if type(column_def) == str:
            column_defs_list.append({
                'title': column_def,
                'targets': index,
                'orderable': 1,
                'searchable': 1
            })
        elif type(column_def) == dict:
            column_def['targets'] = index
            column_defs_list.append(column_def)

    return column_defs_list
