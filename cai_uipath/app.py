#!/usr/bin/env python3.6

from flask import Flask, request, jsonify, render_template
import json, requests, time

class Robot:
    def __init__(self):
        self.access_token = ''
        self.req_data = None
robot = Robot()


app = Flask(__name__, static_url_path='/static')


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html') # use methods = GET


def get_access_token():
    oauth_url = 'https://account.uipath.com/oauth/token'

    data = json.dumps({
        'refresh_token' : 'FoIvISJddVJJ4ivr-QBUZumSlwIyoQnP8wmhFmSy_A2pv', #self.refresh_token,
        'client_id' : '5v7PmPJL6FOGu6RB8I1Y4adLBhIwovQN', #self.client_id,
        #client_secret=self.client_secret,
        'grant_type' : 'refresh_token'
        })

    headers = {'content-type': 'application/json'}

    response = requests.post(oauth_url, data=data, headers=headers)
    print(response)
    print(response.status_code, response.reason)
    response = response.json()
    robot.access_token = response.get('access_token')
    # print(robot.access_token)

    # get_access_token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsImtpZCI6IlJUTkVOMEl5T1RWQk1UZEVRVEEzUlRZNE16UkJPVU00UVRRM016TXlSalUzUmpnMk4wSTBPQSJ9.eyJodHRwczovL3VpcGF0aC9lbWFpbCI6Imh1dy53YXNvbkB1ay5mdWppdHN1LmNvbSIsImh0dHBzOi8vdWlwYXRoL2VtYWlsX3ZlcmlmaWVkIjp0cnVlLCJpc3MiOiJodHRwczovL2FjY291bnQudWlwYXRoLmNvbS8iLCJzdWIiOiJhdXRoMHw1Y2U3Njg2ZDcxNDBkYzBmNjg5ZWEzNzQiLCJhdWQiOlsiaHR0cHM6Ly9vcmNoZXN0cmF0b3IuY2xvdWQudWlwYXRoLmNvbSIsImh0dHBzOi8vdWlwYXRoLmV1LmF1dGgwLmNvbS91c2VyaW5mbyJdLCJpYXQiOjE1NjQ0ODY3NzYsImV4cCI6MTU2NDU3MzE3NiwiYXpwIjoiNXY3UG1QSkw2Rk9HdTZSQjhJMVk0YWRMQmhJd292UU4iLCJzY29wZSI6Im9wZW5pZCBwcm9maWxlIGVtYWlsIG9mZmxpbmVfYWNjZXNzIn0.WVzmMisOmN4yd-vlDSoKrLe0dP-e6JNeKvLIKRdLECf27BX-gWjNNzN_YTR7pfP487-ceuuSoygFqaKzDBjE9_1Gxbc_ejANv03x8pCzBf-3W3MQlz0B2aRz5fWCUqzaU-sDVlU01WN7QVJ3o1sTDQyBcOF0uv1M8OHh_c19gg_o0GwWStJp-8O_vpsSxsphqFt7DfvHpnqHDQLEJKRPQYSmHuNDm8qPP4PrFsk86ViqUMo_dGjfKp9zSTy4OjHHpTtvoCwpPbm2uFc_qrhsxo1Z-kgppomSNOMD2vbK09SzmeWX_Wta_01D9Tje0Z1Xl9UoWOMam6l5pVkmeY_9uA'
    # start_job(get_access_token)

    # answer = 'Roger That!'
    # return respond(answer)


# testing
# @app.route('/start_job2', methods=['POST'])
# def start_job2():
#     bot_data = json.loads(request.get_data().decode())
#     # wait here for the result to be available before continuing
#     while robot.req_data is None:
#         pass
#     print(robot.req_data)
#     return respond(robot.req_data)

@app.route('/start_job', methods=['POST'])
def start_job():
    answer = 'default'
    bot_data = json.loads(request.get_data().decode())
    query = bot_data["nlp"]["source"]
    print(type(query))

    if robot.access_token == '':
        print('must get token')
        get_access_token()

    # query = 'Apple TV 3'
    print(query)

    url = 'https://platform.uipath.com/odata/Jobs/UiPath.Server.Configuration.OData.StartJobs'
    data = { "startInfo":
                       { "ReleaseKey": "d22440e3-3426-4838-9ced-67e01e517f21",
                         "Strategy": "Specific",
                         "RobotIds": [ 207466 ],
                         "NoOfRobots": 0,
                         "Source": "Manual",
                         'InputArguments': '{"in_argument":"' + str(query) + '"}'
                            }}

    headers = {
        "X-UIPATH-TenantName": "TrainingHW",
        "Content-Type": "application/json",
        "Authorization": "Bearer {}".format(robot.access_token)
    }

    print(data['startInfo'])
    response = requests.post(url, data=json.dumps(data), headers=headers)
    print(response.status_code, response.reason)

    response = response.json()
    print(response)
    job_id = response['value'][0]['Id']
    print('job ID: {}'.format(job_id))


    url2 = 'https://platform.uipath.com/odata/Jobs?$filter=Id%20eq%20' + str(job_id)
    state = ''

    # wait here for the result to be available before continuing
    #while robot.req_data is None:
    while state != 'Successful':
        time.sleep(10)
        answer = requests.get(url2, headers=headers)
        answer = answer.json()
        print(answer)
    print(answer)
    return respond(answer)
    # return respond(robot.req_data)


# incoming webhook for uipath to call
@app.route('/incoming', methods=['POST'])
def incoming():
    json = request.get_json()
    robot.req_data = json
    return json


def respond(answer):
    return jsonify(
    status=200,
    replies=[{
      'type': 'text',
      'content': '%s' % (answer)
    }],
    # conversation={
    #   'id' : robot.conversation_id,
      # 'memory': { 'name': value}
    # }
)

@app.route('/errors', methods=['POST'])
def errors():
  print(json.loads(request.get_data().decode()))
  return jsonify(status=200)


if __name__ == "__main__":

    # local testing
    app.run(debug=True, host = '0.0.0.0', port = 5000)

    # for Heroku deployment
    #port = int(os.environ['PORT'])
    #app.run(port=port, host="0.0.0.0")
