def _generate_message_json():
        return {
            "messaging_product": "whatsapp",
            "to": "51",
            "type": "template",
            "template": {
                "name": "message_send_document",
                "language": {
                    "code": "en_US"
                },
                "components": [
                    {
                        "type": "header",
                        "parameters": [
                            {
                                "type": "document",
                                "document": {
                                    "filename": "Nombre!",
                                    "link": "Link"
                                }
                            }
                        ]
                    },
                    {
                        "type" : "body",
                        "parameters": [
                            {
                            "type": "text",
                            "text": "MEssage"
                            }
                        ] 
                    }
                ]
            }
        }
msg_json = _generate_message_json()
print(10 * "=")
print(msg_json['template']['components'][1])
print(10 * "=")
print(msg_json['template']['components'][1])
