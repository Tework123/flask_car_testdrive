schema_get_users_example = {
    "type": "object",
    "properties": {
        "data": {"type": "array",
                 "items": {
                     "type": "object",
                     "properties": {
                         "id_user": {"type": "integer", "description": "User id"},
                         "country": {"type": "string", "description": "Country people"},
                         "last_seen": {"type": "string", "description": "Last seen"}
                     },
                     "required": ["id_user", "country", "last_seen"]
                 }}}}