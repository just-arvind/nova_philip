import swagger_client
from flask import Flask
from src.config_app import *
import requests
import threading
from flask_cors import CORS
import json
from swagger_client.rest import ApiException

def generate_token():
    api_instance = swagger_client.AuthorizationApi()

    try: 
        api_response = api_instance.api_authorize_post(USER_LOGIN, USER_PASSWORD)
        token_nova = api_response['d']['access_token']
        token_status_code = 1
        return token_nova, token_status_code
    except ApiException as e:
        error_response = f"Exception when calling AuthorizationApi->apiAuthorizePost: %s\n" % e
        token_status_code = 0
        return error_response, token_status_code

def search_in_global(id_value):
    global overall_response
    response = next((i for i, item in enumerate(overall_response) if item["id"] == id_value), None)
    return response

def updating_data():
    global overall_response
    print("Running updation..")
    target_url = PHILLIPNOVA_TARGET_URL

    # token_from_user = request.cookies.get('nova_phillip_token')
    auth_token, status_code = generate_token()
    if not status_code:
        print("Access token generation failure !")
        return

    response_obj_stream = requests.get(target_url, headers={'authorization': auth_token}, stream=True)
    for_run_counts = 1
    # complete response values
    c_res = RESPONSE_OBJ_FE
    f_value_list = []

    for line in response_obj_stream.iter_lines():
    # filter out keep-alive new lines
        # print("Iterating lines...")
        if line:
            decoded_line = line.decode('utf-8')
            json_data = json.loads(decoded_line)

            # print(json_data)

            if for_run_counts >= 1 and for_run_counts <= 3:
                c_res.update(json_data)
                f_value_list.append(json_data['f'])

            if for_run_counts == 3:
                # value updation
                c_res['f'] = f_value_list

                # searching and replacement
                search_result = search_in_global(c_res['id'])

                if search_result is None:
                    overall_response.append(c_res.copy())
                else:
                    overall_response[search_result] = c_res.copy()
                # --

                # reseting values
                c_res = RESPONSE_OBJ_FE
                for_run_counts = 1
                f_value_list = []
                # ---
            
            for_run_counts += 1
            # print(overall_response)


api_instance = swagger_client.AuthorizationApi()

app = Flask(__name__)
CORS(app)

overall_response = []


# @app.route('/get_token')
# def get_token():
#     try:
#         token_api_response = api_instance.api_authorize_post(USER_LOGIN, USER_PASSWORD)
#         print("Token fetched !")
#     except ApiException as e:
#         expection_info = "Exception when calling AuthorizationApi->apiAuthorizePost: %s\n" % e
#         return expection_info
    
#     res = make_response("Token generated successfully !")
#     res.set_cookie('phillip_nova_token', 'token_here')

#     return res


@app.route('/')
def homepage():
    return "API is up !"


@app.route('/get_data')
def get_data():
    return_obj = {'phillip_nova': overall_response}
    return return_obj


if __name__ == '__main__':
    data_updating_thread = threading.Thread(target=updating_data)
    data_updating_thread.start()
    # app.run(host='0.0.0.0', port=5080)
    app.run(host='localhost', port=5080)