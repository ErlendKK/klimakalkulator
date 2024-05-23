# @app.route('/api/data', methods=['GET'])
# def get_data():
#     headers = {
#         'Authorization': f'Bearer {ECOPORTAL_API_TOKEN}'
#     }
#     response = requests.get(f'{PATH}', headers=headers)

#     if response.status_code == 200:
#         try:
#             data = response.json()

#             # Filtrer data basert på "classific" som inneholder ordet "Bygg"
#             print("Data fetched successfully:")
#             emission_factors = extract_emission_factors(data)
#             print(emission_factors)
#             return jsonify(data)
        
#         except ValueError:  # Catch JSON decoding errors
#             print("Decoding JSON has failed")
#             return jsonify({"status": "failed", "message": "Decoding JSON has failed"}), 500
#     else:
#         print("Failed to fetch data")
#         return jsonify({"status": "failed", "message": response.status_code}), response.status_code

# @app.route('/set_test_cookie')
# def set_test_cookie():
#     resp = make_response("Cookie set")
#     resp.set_cookie('test', 'value')
#     return resp

# def fetch_emission_factor_from_ecoportal(uuid):
#     headers = {
#         'Authorization': f'Bearer {ECOPORTAL_API_TOKEN}'
#     }
#     response = requests.get(f'{ECOPORTAL_BASE_URL}{uuid}?format=JSON', headers=headers)

#     if response.status_code != 200:
#         print("Failed to fetch data")
#         return []
    
#     try:
#         lca_data = response.json()
#         emission_factors = extract_emission_factors(lca_data)
#         return emission_factors
    
#     except ValueError:
#         print("Failed to decode JSON")
#         return []   





# uuid_list = [
#   "94506cde-817c-4307-bef0-4a317b894e95",
#   "19d94e69-362b-48b0-8130-71c9b7a43ad6",
#   "58871b96-bcdf-4438-b82f-d100c1df1fe5",
#   "982ea073-82cb-4515-aa4f-b2f7381105af",
#   "5100c688-3a97-41b7-9223-d58916b04870",
#   "5ace36b6-9f29-41a0-b4d6-b7fc6ba3f8ff",
#   "f7283e72-d54f-4637-a1a8-368362a63f13"
# ]
# QUERY_STRING = '?format=JSON&view=extended'
# PATH = 'https://epdnorway.lca-data.com/resource/processes/a1db2cb9-fe80-4e27-85a5-8c574f6c3003?format=JSON&view=extended'