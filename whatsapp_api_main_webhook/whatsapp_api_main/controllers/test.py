import requests
import json
head = {
        "Content-Type": "application/json",
        "Authorization" : "Bearer 30cca545-3838-48b2-80a7-9e43b1ae8ce4"
    }

data = {
    "db_name" : "db_prueba",
    "user_name" : "JouCode",
    "message" :  {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": "51935548928",
            "type": "text",
            "text": {
                "preview_url": False, 
                "body": "Helloo"
            }
    }
}

response = requests.post('http://192.168.2.21:8069/api/home', headers=head, json=data)
my_json = response.content.decode('utf8').replace("'",'"')

data = json.loads(my_json)
s = json.dumps(data, indent=4, sort_keys=True)
print(data['result']['message'])

# headers = {
#             "Content-Type": "application/json",
#             "Authorization": "Bearer {}".format(data['result']['token']),
# }
# r = requests.post(f"{data['result']['url']}", headers=headers, json=data['result']['message'])
# print(r.content)