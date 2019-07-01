import fastjsonschema


route_file_schema = {
    '$draft': 'draft-07',
    'type': 'object',
    'properties': {
        'routes': {
            'type': 'array',
            'minItems': 1,
            'items': {
                'type': 'object',
                'properties': {
                    'instructions': {
                        'type': 'array',
                        'minItems': 2,
                        'items': {
                            'oneOf': [
                                {
                                    'type': 'array',
                                    'items': [
                                        {'type': 'string', 'enum': ['START']},
                                        {
                                            'type': 'array',
                                            'minItems': 2,
                                            'maxItems': 2,
                                            'items': {'type': 'integer', 'minimum': 0},
                                        },
                                    ],
                                    'additionalItems': False,
                                },
                                {
                                    'type': 'array',
                                    'items': [
                                        {'type': 'string', 'enum': ['GO']},
                                        {
                                            'type': 'array',
                                            'items': [
                                                {
                                                    'oneOf': [
                                                        {'type': 'string', 'enum': ['N', 'E', 'S', 'W']},
                                                        {'type': 'null'},
                                                    ]
                                                },
                                                {'type': 'integer', 'minimum': 0}
                                            ],
                                            'additionalItems': False,
                                        },
                                    ],
                                    'additionalItems': False,
                                },
                                {
                                    'type': 'array',
                                    'items': [
                                        {'type': 'string', 'enum': ['TURN']},
                                        {'type': 'string', 'enum': ['L', 'R']}
                                    ],
                                    'additionalItems': False,
                                },
                                {
                                    'type': 'array',
                                    'items': [
                                        {'type': 'string', 'enum': ['REACH']},
                                        {'type': 'string', 'minLength': 1},
                                    ],
                                    'additionalItems': False,
                                },
                            ],
                        },
                    },
                    'landmarks': {
                        'type': 'array',
                        'items': {
                            'type': 'object',
                            'properties': {
                                'coordinate': {
                                    'type': 'array',
                                    'minItems': 2,
                                    'maxItems': 2,
                                    'items': {'type': 'integer', 'minimum': 0},
                                },
                                'name': {'type': 'string', 'minLength': 1},
                            },
                            'required': ['coordinate', 'name'],
                            'additionalProperties': False,
                        },
                    },
                },
                'required': ['instructions', 'landmarks'],
                'additionalProperties': False,
            },
        },
    },
    'required': ['routes'],
    'additionalProperties': False,
}

route_file_validator = fastjsonschema.compile(route_file_schema)
