prescriptionsSchema = {
    "type" : "object",
    "properties": {
        "clinic": {
            "type": "object",
            "properties": {
                "id": {"type": "integer"}
            },
            "required": ["id"]
        },
        "physician": {
            "type": "object",
            "properties": {
                "id": {"type": "integer"}
            },
            "required": ["id"]
        },
        "patient": {
            "type": "object",
            "properties": {
                "id": {"type": "integer"}
            },
            "required": ["id"]
        },
        "text": {"type": "string"}
    },
    "required": ["clinic", "physician", "patient", "text"]
}
