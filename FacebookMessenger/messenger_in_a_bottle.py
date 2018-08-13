import json
import requests

from bottle import debug, request, route, run

GRAPH_URL = "https://graph.facebook.com/v2.6"
VERIFY_TOKEN = 'EAACLjXSL7EkBANeQ2ZBNP5HE9daM2zZCAI7pugrQoOU8qiRUDwu6haS25'
PAGE_TOKEN = 'EAADNo5oP7wgBACxIZBuoMC8daJh9JmnCTvmTwpZAsD6m3lCFT3TnNn2T4DUNFOxqtVcrX8GDN3flnwKDpOyvnYtFUkoUbYRCURZAUWbKlLBYhOOcZBfv2Sy0PYDsw3vOaINWGl3Wg1wWCL6oxukZCiBwCcPxwCg8tjKTK4BZAkcAZDZD'

def send_to_messenger(ctx):
    url = "{0}/me/messages?access_token={1}".format(GRAPH_URL, PAGE_TOKEN)
    response = requests.post(url, json=ctx)

@route('/chat', method=["GET", "POST"])
def bot_endpoint():
    if request.method.lower() == 'get':
        verify_token = request.GET.get('hub.verify_token')
        hub_challenge = request.GET.get('hub.challenge')
        if verify_token == VERIFY_TOKEN:
            url = "{0}/me/subscribed_apps?access_token={1}".format(GRAPH_URL, PAGE_TOKEN)
            response = requests.post(url)
            return hub_challenge
    else:
        body = json.loads(request.body.read())

        print body
        
        user_id = body['entry'][0]['changes'][0]['value']['to']['data'][0]['id']
        page_id = body['entry'][0]['id']
        message_text = body['entry'][0]['changes'][0]['value']['message']
        
                    
        # we just echo to show it works
        # use your imagination afterwards
        if user_id != page_id:
            ctx = {
                'recipient': {
                    'id': user_id,
                },
                'message': {
                    'text': message_text,
                }
            }
            response = send_to_messenger(ctx)
        return ''


debug(True)
run(reloader=True, port=8088)