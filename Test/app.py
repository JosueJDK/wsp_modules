
def _generate_save_message_json(status_code, number_phone, component_text=False, component_document=False):
        if component_text and component_document:
            return {
                "type" : "save_message",
                "db_name" : "prueba",
                "user_name" : "joucode",
                "message_data" : {
                    "messaging_product": "whatsapp",
                    "recipient_type" : "individual",
                    "recipient_id" : "51" + number_phone,
                    "status_code" : status_code,
                    "type_message" : "template",
                    "text_message" : component_text['parameters'][0]['text'],
                    "link_file" : component_document['parameters'][0]['document']['filename'],
                    "filename" : component_document['parameters'][0]['document']['link']
                }
            }
        elif component_text:
            return {
                "type" : "save_message",
                "db_name" : "prueba",
                "user_name" : "joucode",
                "message_data" : {
                    "messaging_product": "whatsapp",
                    "recipient_type" : "individual",
                    "recipient_id" : "51" + number_phone,
                    "status_code" : status_code,
                    "type_message" : "template",
                    "text_message" : component_text['parameters'][0]['text']
                }
            }
def create_message_components_header(file_document, link_document):
        return {
                "type": "header",
                "parameters": [
                    {
                        "type": "document",
                        "document": {
                            "filename": file_document,
                            "link": link_document
                        }
                    }
                ]
            }

def create_message_components_body(message):
    return {
            "type" : "body",
            "parameters": [
                {
                "type": "text",
                "text": message
                }
            ] 
        }

component_text = create_message_components_body("Helllo!")
component_header = create_message_components_header("Prueba!", "link file!")
print(_generate_save_message_json("200", "935548928", component_text))