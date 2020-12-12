prescriptionsInputSchema = {
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


prescriptionsOutputSchema = {
    "type" : "object",
    "properties": {
        "data": {
            "type": "object",
            "properties" : {
                **prescriptionsInputSchema["properties"],
                "id" : {"type": "object"}
            },
            "required": [*prescriptionsInputSchema["required"], "id"]
        }
    },
    "required": ["data"]
}


prescriptionsErrorMsgSchema = {
    "type" : "object",
    "properties": {
        "error": {
            "type": "object",
            "properties": {
                "message": {"type": "string"},
                "code": {"type": "string"}
            },
            "required": ["message", "code"]
        }
    },
    "required": ["error"]
}
