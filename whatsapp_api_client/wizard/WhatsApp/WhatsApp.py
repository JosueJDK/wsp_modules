import requests
import json

class WhatsAppMain(object):
    def __init__(self, user_name, token_verify, db_name):
        self._user_name = user_name
        self._token_verify = token_verify
        self._db_name = db_name
        self.url_base = 'https://55ee-181-65-25-75.sa.ngrok.io/api/home'

    def request_whatsapp_api_main(self, data):
        headers = {
            "Content-Type": "application/json",
            "Authorization" : f"Bearer {self._token_verify}"
        }
        response = requests.post(self.url_base, headers=headers, json=data)
        return response.status_code

    def request_authorization_whatsapp(self):
        data = {
                "type" : "authorization",
                "db_name" : self._db_name,
                "user_name" : self._user_name
            }
        return self.request_whatsapp_api_main(data)
    
    def request_save_message_whatsapp(self, data_message):
        return self.request_whatsapp_api_main(data_message)
    
    def send_message_whatsapp(self, response_data, message_json):
        if response_data == 200:
            headers = {
                "Content-Type": "application/json",
                "Authorization" : f"Bearer {self._token_verify}"
            }

            data = {
                "type" : "SendMessageWhatsapp",
                "db_name" : self._db_name,
                "user_name" : self._user_name,
                "message_json" : message_json
            }

            response = requests.post(self.url_base, headers=headers, json=data)
            return response.status_code


    def _generate_save_message_json(self, status_code, number_phone, component_text=False, component_document=False):
        if component_text and component_document:
            return {
                "type" : "save_message",
                "db_name" : self._db_name,
                "user_name" : self._user_name,
                "message_data" : {
                    "messaging_product": "whatsapp",
                    "recipient_type" : "individual",
                    "recipient_id" : "51" + number_phone,
                    "status_code" : status_code,
                    "type_message" : "template",
                    "text_message" : component_text['parameters'][0]['text'],
                    "link_file" : component_document['parameters'][0]['document']['link'],
                    "filename" : component_document['parameters'][0]['document']['filename']
                }
            }
        elif component_text:
            return {
                "type" : "save_message",
                "db_name" : self._db_name,
                "user_name" : self._user_name,
                "message_data" : {
                    "messaging_product": "whatsapp",
                    "recipient_type" : "individual",
                    "recipient_id" : "51" + number_phone,
                    "status_code" : status_code,
                    "type_message" : "template",
                    "text_message" : component_text['parameters'][0]['text'],
                    "link_file" : "",
                    "filename" : ""
                }
            }
        else:
            return {
                "type" : "save_message",
                "db_name" : self._db_name,
                "user_name" : self._user_name,
                "message_data" : {
                    "messaging_product": "whatsapp",
                    "recipient_type" : "individual",
                    "recipient_id" : "51" + number_phone,
                    "status_code" : status_code,
                    "type_message" : "template",
                    "text_message" : "",
                    "link_file" : "",
                    "filename" : ""
                }
            }

    def _send_message_template(self, name_template, number_phone, components=False):
        if components:
            return {
                "messaging_product": "whatsapp",
                "recipient_type" : "individual",
                "to": "51" +  number_phone,
                "type": "template",
                "template": {
                    "name": name_template,
                    "language": {
                    "code": "en_US"
                    },
                    "components": components
                }
            }

        else:
            return {
                "messaging_product": "whatsapp",
                "recipient_type" : "individual",
                "to": "51" +  number_phone,
                "type": "template",
                "template": {
                    "name": name_template,
                    "language": {
                        "code": "en_US"
                    }
                }
            }

    def create_message_components_header(self, file_document, link_document):
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

    def create_message_components_body(self, message):
        return {
                "type" : "body",
                "parameters": [
                    {
                    "type": "text",
                    "text": message
                    }
                ] 
            }