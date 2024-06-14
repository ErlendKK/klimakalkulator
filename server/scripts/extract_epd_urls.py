import requests
import json
import os

ECOPORTAL_API_TOKEN = 'eyJhbGciOiJSUzI1NiJ9.eyJzdWIiOiJFcmxlbmQiLCJpc3MiOiJFQ09QT1JUQUwiLCJhdWQiOiJhbnkiLCJ2ZXIiOiI3LjkuNyIsInBlcm1pc3Npb25zIjpbInVzZXI6cmVhZCx3cml0ZTo2ODgiLCJzdG9jazpyZWFkLGV4cG9ydDoyIiwic3RvY2s6cmVhZCxleHBvcnQ6MSJdLCJyb2xlcyI6W10sImlhdCI6MTcxMjU3NTA4NSwiZXhwIjoxNzIwNDU5MDg1LCJlbWFpbCI6ImVybGVuZGtAbGl2ZS5jb20iLCJ0aXRsZSI6ImhoIiwiZmlyc3ROYW1lIjoiRXJsZW5kICIsImxhc3ROYW1lIjoiS3ZpdHJ1ZCIsImdlbmVyYXRlTmV3VG9rZW5zIjpmYWxzZSwiam9iUG9zaXRpb24iOiJFbmdpbmVlciIsImFkZHJlc3MiOnsiY2l0eSI6IlN0YXZhbmdlciIsInppcENvZGUiOiI0MDE2IiwiY291bnRyeSI6Ik5PIiwic3RyZWV0IjoiIn0sIm9yZ2FuaXphdGlvbiI6e30sInVzZXJHcm91cHMiOlt7InVzZXJHcm91cE5hbWUiOiJyZWdpc3RlcmVkX3VzZXJzIiwidXNlckdyb3VwT3JnYW5pemF0aW9uTmFtZSI6IkRlZmF1bHQgT3JnYW5pemF0aW9uIn1dLCJhZG1pbmlzdHJhdGVkT3JnYW5pemF0aW9uc05hbWVzIjoiIiwicGhvbmUiOiI5NzExMTg0MSIsImRzcHVycG9zZSI6IkFuIExDQSB3ZWJhcHAgIiwic2VjdG9yIjoiIiwiaW5zdGl0dXRpb24iOiJWZW5pIn0.ru36AZheBwYK8_N3d9YNBYfLIcEWMtmOV0hNs7a_sgGPheZL9DVrjJXdotypysodIJGTvMd-QqEALyCVOms3ntABTDYB4NCBqydJLTX1H8R8Gu0AvNIldtRxhhrEfEpjzLnv0itddlMuRqYVxB46EAP3eNft4NXqvpyHdJS73Pk'
ECOPORTAL_BASE_URL = 'https://epdnorway.lca-data.com/resource/processes'

def fetch_uuids():
    """fetches EPD UUIDs from Ecoportal"""
    query_string  = '?search=true&validUntil=2024&format=JSON'
    headers = {
        'Authorization': f'Bearer {ECOPORTAL_API_TOKEN}'
    }
    try:
        response = requests.get(f'{ECOPORTAL_BASE_URL}{query_string}', headers=headers)
        response.raise_for_status()
        data = response.json()
        return data
    
    except requests.exceptions.HTTPError as e:
        print(f'FAILED TO FETCH UUIDS: {e}')
        return []
    
    except Exception as e:
        print(f'FAILED TO FETCH UUIDS: {e}')
        return []


def fetch_URL(uuid):
    """Fetches an EPD URL for a given UUID. 
    If none are found, returns an empty string
    """
    query_string = '?format=JSON&view=extended'
    headers = {
        'Authorization': f'Bearer {ECOPORTAL_API_TOKEN}'
    }
    path = f'{ECOPORTAL_BASE_URL}/{uuid}{query_string}'
    
    try:
        response = requests.get(path, headers=headers)
        response.raise_for_status()
        data = response.json()

        # Extract url from response object
        resource_urls = data['modellingAndValidation']['dataSourcesTreatmentAndRepresentativeness']['other']['anies'][0]['value']['resourceURLs']
        print(resource_urls[0])
        return resource_urls[0]
    
    except requests.exceptions.HTTPError as e:
        print(f'FAILED TO FETCH EPD URL: {e}')
        return ""
    
    except Exception as e:
        print(f'FAILED TO FETCH EPD URL: {e}')
        return ""


def create_epd_url_json(uuids):
    """Creates a JSON file with UUID and URL pairs.
    """
    uuid_url_pairs = {}
    for uuid in uuids:
        url = fetch_URL(uuid)
        uuid_url_pairs[uuid] = url

    print(uuid_url_pairs)
    with open('epd_urls.json', 'w') as f:
        json.dump(uuid_url_pairs, f, indent=4)
    print("EPD URL JSON file created successfully.")


def load_epd_urls(filename):
    """Load the EPD URL data from a JSON file."""
    try:
        os.chdir('server')
        with open(filename, 'r') as file:
            epd_urls = json.load(file)
        print("Loaded URLs:", epd_urls) 
        return epd_urls
    except FileNotFoundError:
        print("The file was not found.")
        return {}
    except json.JSONDecodeError:
        print("Failed to decode JSON.")
        return {}


def fetch_urls_for_uuids(uuids, epd_urls):
    """Fetch URLs for a list of UUIDs using the EPD URL data."""
    url_data = {}

    for uuid in uuids:
        url = epd_urls.get(uuid)
        if url:
            url_data[uuid] = url
        else:
            url_data[uuid] = "URL not found"
    return url_data


uuids_test = [
    '94506cde-817c-4307-bef0-4a317b894e95',
    '19d94e69-362b-48b0-8130-71c9b7a43ad6',
    '58871b96-bcdf-4438-b82f-d100c1df1fe5',
    '982ea073-82cb-4515-aa4f-b2f7381105af',
    '5100c688-3a97-41b7-9223-d58916b04870',
    'f7283e72-d54f-4637-a1a8-368362a63f13',
    '503dfca1-7c65-4179-9ffa-ebc6d8b48b7d',
]

# Fetch the URLs
epd_urls = load_epd_urls('epd_urls.json')
fetched_urls = fetch_urls_for_uuids(uuids_test, epd_urls)
print(fetched_urls)


# Full list of UUIDs
uuids = [
    '94506cde-817c-4307-bef0-4a317b894e95',
    '19d94e69-362b-48b0-8130-71c9b7a43ad6',
    '58871b96-bcdf-4438-b82f-d100c1df1fe5',
    '982ea073-82cb-4515-aa4f-b2f7381105af',
    '5100c688-3a97-41b7-9223-d58916b04870',
    'f7283e72-d54f-4637-a1a8-368362a63f13',
    '503dfca1-7c65-4179-9ffa-ebc6d8b48b7d',
    'de61692f-47e9-4f6c-827b-79293b9472ba',
    '9a087d3d-e3bf-4629-a107-01baab293bdf',
    '6b14dc2b-65e7-494a-aad2-2926024b2856',
    '8dd11ac5-3192-4c32-b419-0e96b1234844',
    '06f4050b-cb0c-4920-978f-9d588f8ce12c',
    'f67cf9cc-0f6e-4f45-b61a-fe09b2f80622',
    '171d9a9e-3395-41d9-976f-1504153c20c9',
    '4263a30e-0624-4da8-a870-9a5817d75ee1',
    'b8c2a84d-b0bf-4990-851f-d543d7025059',
    '1635ddcc-3c27-4cd5-a486-5b1d602edf82',
    '214b178e-8740-47e8-bc3b-515daeaecda3',
    'ea5b0868-3c16-41f9-8c48-de7e65fd7ff8',
    '98d60725-5759-46a5-99c0-168046ec9432',
    '95233b2b-5b21-4868-a508-e2813bd4c78c',
    '627b52c5-aee6-443e-84ea-e81a8c825d1a',
    'e7f28405-6df3-4ba0-b68a-1bcadbbec220',
    '4895e95e-976e-44b9-a405-36ab28061749',
    '9212840b-43fe-486d-9b53-8850a06a6e28',
    '5739d50f-1a92-404b-a316-f558bc9989fe',
    '4f2d4609-a9e8-4bed-9f52-b51ff06f0dba',
    'dbed8802-50c3-4a50-b977-76634f18aaee',
    '6d732a71-9c30-4d6c-85b6-440fcc04397d',
    '4499502f-65a3-4df1-b313-2da30db77173',
    '47a78a20-5390-4ca9-baf2-5102983a8600',
    'c63a697f-d454-4d5e-9d87-86e5eca2b328',
    'a6154801-46e9-4415-a139-744ee2743f25',
    '35772fa2-db41-44f0-bae3-fdf2d03907d6',
    '0befe9f7-e74b-4650-bd06-03ab165a70d1',
    'b9cd60bb-0be1-4796-9327-caf79984c86a',
    'f7b7d737-3743-4d76-9bac-13613203e299',
    'c5ca8d8d-03df-4bf5-9cf6-9d76812dd558',
    '5b7d830e-ecce-46c4-a0e3-db49ec371a26',
    'b40a12e6-ba90-46df-ac75-5412eb9b5e3d',
    'f701626e-8d80-4f72-86f5-bdcf562c5e89',
    'fcbb5957-424c-4d08-8d94-7707cd57be2b',
    '57786cf2-5a18-47f4-8f38-66fb62ed1029',
    '464fd9f7-3c7a-43a1-975f-05394d78091f',
    '773a4053-88ba-4eb3-ad1a-39f6c198b9ef',
    '0ffb812c-f5f7-4e8f-a074-e1adba7d3cce',
    'c6da3f34-515b-4f49-8610-e1c44ac9fdaa',
    'fd488aa2-89ec-418a-9a23-319aee1fcaa4',
    '520a384b-a74a-4f72-b872-5c764e86ccc2',
    'bf3b4f5a-b8a8-43e0-be4e-d99d950c8303',
    '133a400e-ea6f-43ae-b992-011b09afbf05',
    '2b13f64e-f51c-4a24-9855-e848584dc8d6',
    '9ca3ab10-8215-4121-8053-4af5907886af',
    'b1e44f7b-5c63-4d34-8522-307fed2cc0a9',
    '452f0af2-e7ef-466f-b74d-b250ea271d09',
    '4a14f5f5-11a7-4095-8f32-9c92921222c4',
    'be203331-840d-430b-a49e-fffed9a4f4f1',
    'b725bea7-f54b-4107-aed8-3a96a8a0cb05',
    'fe7d4dfe-6ce2-4090-8c13-43352638f394',
    '4dfe0971-f707-49b9-a311-055ac035bf85',
    '11ca796b-aaf7-4fb2-ad09-cf0217a9d41b',
    'a1db2cb9-fe80-4e27-85a5-8c574f6c3003',
    '6dfb478b-45dd-426a-8e81-3a2b08e19350',
    'e25280d4-ab92-4592-9af8-5fea9c608032',
    'ea5622f2-81be-4a1f-a14b-b6dda7aa6555',
    '5748e8c2-39ca-44e0-a88b-4cab3d1aea04',
    '358041a6-c02e-4a22-bf20-dac203bcad34',
    '68adc1f8-24e0-402f-b452-9134f9ba6725',
    '81f94a08-4306-4f7b-97db-e213bd1a7774',
    'f3715898-6d32-4f9c-aa34-fc2a79355424',
    '6ae41a15-e2b9-4f18-89de-b5dbe662ed18',
    'a801b923-f1f8-4727-94ea-687413c72000',
    '261188b8-ca5b-4074-803d-c272d0a70506',
    '7a4fda07-c95c-4a54-b4a3-47855c720de9',
    '0fd331fd-a92c-4662-9c0c-f0c7f2733111',
    '6d790d6f-9ea2-48df-ab66-c7e1deae1165',
    '9975a2e1-0fe5-4e0b-af36-26688b718f6e',
    '1df22743-7e61-4c19-a1d5-e2434428e555',
    '889c149d-1c7f-42aa-8668-73a95f6e9081',
    '8665cfc8-498c-4c7e-981b-3c48dbc970b4',
    '58476c51-01e2-4866-bd27-d665341f09fe',
    'f0da776f-824d-4890-b10a-4ef44fec3bea',
    'b240a5c2-be46-4fcd-b241-ab7121f7820f',
    '98c10430-e041-4f10-a70e-7ed9d6cd64b4',
    '56b96a4f-123f-48af-bcb4-95c0ddc3d7ca',
    '8dae6b30-af75-4756-9f4b-a37ec2edd316',
    '04a74ab7-0712-4888-be2d-26f2e90b51fc',
    '75663386-52eb-455b-8b37-f908dd863bbf',
    '89274bea-96fe-4599-b2c5-9f64f44091e3',
    '71dcf63c-8c1d-48ad-a7db-29d34088a815',
    '81cf18c4-c121-4959-b84c-6fada9295460',
    '0dd49462-4c11-4388-aeef-bb54d59e49c5',
    '9d4e39e6-644e-4d65-8ebe-2574d6b3d1c0',
    'df4904e5-b95e-4ce4-becb-2db1c59792a2',
    'c055096f-b610-4bab-8457-e24728fde344',
    '578736db-f5f8-4cdb-9a05-fc25f558f85c',
    '2b4bddfa-1316-4b23-8a8c-43f0d0af8d59',
    'f4d994ea-8969-4b94-95cd-b93e37eb4b26',
    'ab009554-a36f-4f7f-a32c-df2d256a7fc5',
    '3cf34fc0-80f2-4344-b051-aa76aa7081d0',
    'f3ef3030-864f-4277-82c3-c0243701728b',
    '8269258e-2236-4345-a5e4-887212663287',
    '2511c42f-d76d-4668-8073-67c81dbdcd99',
    '2772a90d-d974-4587-8bb1-1ef627767764',
    '585b5755-b9fd-45f2-80e2-66b10c835d13',
    '89da485e-e083-4c3d-a735-391b5ba31ab6',
    'a49ed7a0-5bb8-4a7b-adf5-26927296d941',
    '42c5fa5f-2c7a-4f1f-870e-574905793f95',
    '61223567-0ac3-43d4-83e0-5b546ea02ddd',
    '5aff4cf5-c765-40a1-a460-4ab3ebbda900',
    '5b924892-dfb0-4019-b955-5caddc84e7f9',
    '64568f33-ad29-40db-a3ee-7f00e88992c1',
    '3f7c616d-2523-473a-a9e6-6482b1ada4d7',
    'd2b75821-d34b-4202-b9cd-39924c5082cc',
    'ad8f14d3-c0b9-4f0c-a39e-e15065b785f3',
    '6c7ca93f-42af-461c-8a9b-fefffc736221',
    'e6230a24-7cb0-428e-86f1-08cd898ac783',
    '71a77881-f678-4378-a858-a555077ae000',
    'cd1f0b21-4e1e-4425-9a4f-c77f72cf054d',
    '176384c9-a597-4f62-9115-7916953dbd26',
    'f837ce51-9ca1-427f-bb34-4115c14ff5f2',
    '02950ff3-055e-446c-93c4-936e35279cd9',
    '17420ee0-629c-46c0-860d-2281f57d1620',
    '0db1875a-3563-4756-a930-7a315229ae5f',
    '2ad69921-5452-4a1f-8893-aef31e783e3b',
    'caa2251d-7738-49ce-9b23-445b1e3dbcf8',
    '01145859-af70-4f30-96ab-f4a8f3e92f9d',
    '676cd3b4-fb40-4318-80f0-7df77f83ca55',
    'a2995b2d-7fd3-460b-95ae-5c6f45c0b07d',
    '99d45706-f7fc-4cb7-ac15-5d480c431885',
    'd320f189-9a4b-4cac-aaf7-605738e139a3',
    'eb1aa483-9bec-4ce9-8e08-267ccea4638d',
    'ce417ca5-64e5-4526-97b5-99620e6d1225',
    'ccd6ebca-15ca-4c18-a906-b5876f8a7ef2',
    '83833222-865c-4bbe-8c07-dbf439fe8676',
    '6827bfae-b7dd-4dd7-b9ba-4f2f1f660aba',
    'ef6f7c13-471b-4a31-81f0-f04abe1ddb24',
    'b44cd475-5278-4b55-85bf-5c7ae0bd2b22',
    '96f38a5d-507b-4047-a69a-6d4e4248f295',
    'f0c7faa6-21b6-46d3-8442-a58b9827b4ef',
    '048103a7-40be-41cb-80c2-760bf98c00c3',
    '4a47cd4a-401f-475b-a8c2-0e7198359759',
    'd4f66366-1679-4ea2-ba18-23481c58107b',
    'aacb0e2a-7f39-4e5c-a21c-c3bcc0aec785',
    '9fd17334-163b-4494-bb83-0e4fdb5afc94',
    '8cb3cbfa-41cb-4879-af13-05dc69d891ba',
    'b1abf577-b513-41a4-815a-14b3fb83df8c',
    '3912c710-1641-4357-9562-28a5b1ec58fb',
    '0617fc93-37a0-48e5-8161-2b723057dbc8',
    '7b5f96f8-1520-4e93-bdb8-082fb3087369',
    '0ac91dc8-b8c8-4aa3-9855-bb79aafb17db',
    '2895ab9f-1d49-455f-8c26-96aecf2e4d9a',
    'b5d7e9b6-cae8-4fea-935f-7f4f12c9cc88',
    '91902bac-8090-47b6-856d-1f09989be92f',
    'b5b26e71-4a04-446a-ac74-44e00e4c9d38',
    'd6d82a18-852e-415f-99b3-ff4411a8fb25',
    'ebadd145-8fbe-4c1a-9952-737543a36c01',
    'b471b12f-56e3-40c8-8317-523d0d4050a1',
    '08557e13-0a09-4798-a035-0f037d2e25cf',
    'cfbbaac8-b4b7-4e36-aa02-91c54a389683',
    'e38e8922-4bbf-4bac-81a4-3feabd8ab766',
    'c8fe599d-bfed-4cac-ba75-114628791000',
    'de59fc3d-cc0e-45e6-9843-52bce0e778ae',
    '7313a275-77d8-451d-b2e8-ddb7055d38dd',
    '552d80a2-c62f-49dd-b31f-79dc189c6e79',
    'f877a598-6ce2-43d5-8246-40a7afc9d5f9',
    '490cddfc-fff2-4b37-8246-fbfdd8a3b376',
    '08606da9-1b97-41df-81bc-a2a8d58bc931',
    '24257f8f-4327-4579-b0d0-4a86150ab4c6',
    'e67068b8-e73c-438a-8295-9d460b3fe2fb',
    '282e2d7d-5880-430d-9f01-fc0361c2fd34',
    'ff424d09-5d82-4da6-96b5-2f7effe00951',
    '6b0c3450-cbf9-4873-a67f-be3dd0402e10',
    '7606db54-62ed-4932-82e2-8003776ee494',
    'f5adba57-2c55-4072-ae19-04913f5c9fe2',
    'd9c4fd91-2127-4f27-b495-d83f00ebce75',
    'ebb970bd-affc-425a-9243-9ee9edcec355',
    '9abe0571-eed9-484b-8ef5-9f948db91ec9',
    'b85b206d-9373-411b-896e-6d8ee713e715',
    '90024685-ee87-45e8-90eb-9f59b3d3b1f8',
    'a852a144-34b6-4674-8812-96652005558b',
    '1b9e6c8e-97b4-432e-a197-870e7096a8c0',
    '04377811-b78b-4b3e-b4e8-d108636ac797',
    '3347369c-6085-493a-b8ee-a11d4d8cb555',
    '0252a998-24dc-4464-afef-96d8c5d86205',
    '850dd9c5-cbb3-4afe-9075-1d77322dfb7a',
    '919b4f2b-7bfb-41cb-8d37-a95b5cfcea7f',
    '1cd6de7a-5a62-40ff-bfc6-34af2519ce83',
    'a044af2c-17fa-4865-b9ab-ffead7d30474',
    '96883b12-753b-45b8-8c90-ba79693b0979',
    '6967cabe-fbdf-45ed-aab6-5c18fa9b9e32',
    'e5c188af-be82-470a-8ed2-68e890d5dce7',
    'db6985b4-f069-45e4-b7ee-d71868a8e46f',
    '74a9f2dd-7eeb-430f-a3eb-12ef1b4d7d2c',
    'f9bc75c2-fa7c-44ff-905b-bbd0bc4430a1',
    '320b9bee-211c-449a-86d0-ac71a91750da',
    '2e44de9b-e6bc-46a8-b463-7b5e87259baf',
    'b8115428-7336-48e3-bca2-a92b5852b8e1',
    '406c2932-2c0f-4b45-863c-20cfc170fa34',
    '32311573-87af-46d0-8ca9-10120152be74',
    '5a9bff23-4c70-413e-989b-d5a29f5d9f73',
    '53af707c-6933-40b3-acf9-a0f1230d41d0',
    '7011c502-ffde-487b-96db-506de809a3b5',
    '5a281e90-9e18-4cb0-bc0f-b1e850341a95',
    '076a8ff8-63f6-417d-997a-0ca648b66b7f',
    '995d03cc-0901-47d4-8a6d-3978ca48f5b0',
    '27fd0c5b-8774-408a-a476-25d20736724d',
    'c3e859b1-63e1-4ad2-b8e9-0096ae7b95ab',
    'a58582c9-53dd-4a5c-b2d0-a72ad381779f',
    'bb6bf2f0-a7df-4f23-8515-16dd2a405813',
    '88038956-8412-471b-a7ce-4ada8f7bb355',
    '98c978f1-e89a-4eb4-b943-7e00b9614e18',
    '5e4acad3-5149-4cef-9b28-0f011e3ce63a',
    'e9b52b25-c323-4761-b960-a2828b432724',
    'bb603747-d330-47eb-95b9-8b7bc7a1f69b',
    '3da5bbd6-afff-4f87-82fc-8a305cd77bef',
    'fcd1b8f8-3f10-42ee-9486-7d3776f87777',
    '89095d05-0106-4bfe-9521-23f2d407d57e',
    '0f952037-fa76-437e-a42e-efc7ddc23f4f',
    'b554b044-da8e-49a4-8cc5-31a3d492b8a3',
    'e19a3d58-37fc-49c0-a2b4-3108b5ee938b',
    '1d96ff15-8fc2-48c0-9bd2-2014ada80c84',
    '85785399-c2a9-4532-a026-392198d2c658',
    'e668701d-1f0a-4a41-ac77-4467f27ab20c',
    'eef334c9-6800-4200-8da2-3f7c09562b47',
    'f5848681-486e-4a97-9c1b-918103ee0a73',
    '45ca8d72-055b-4c5f-bfeb-ae9a673a11fc',
    'ed94e416-9de0-4046-a9fa-2b71fd28b50c',
    '246b2efb-44b7-4e7a-97cf-bad8249e938c',
    '45f43fe4-6d9e-4c08-857d-0cf6386b0f35',
    '44dadb85-4fbe-43c0-b550-eb1b038043a8',
    '36a0e4b5-22de-4b6c-8dca-ec1b95587c81',
    '19af4711-529e-4955-8fa7-f4c3540e06b9',
    '2d16e5e2-24a6-4c05-98e5-5ce322b0a35c',
    '27cdc5bb-7e00-47dd-b46a-f80db78f3df6',
    'e10c7c95-d2da-490e-b0b0-6cbbfc753a99',
    '6b670147-683b-4813-b662-ad6eedbe7363',
    '9813ae99-b734-4778-83b1-988645606377',
    'eac4d036-5939-4279-b997-35d4e85337d9',
    'f651d733-d6d1-4f67-b14f-b6df5e00a4d2',
    '6dcce577-2d54-442b-8800-c2b4e6a0a2aa',
    '3e70d609-e70f-4b0d-a48c-34639d15c8e0',
    'e08e484e-5463-4e72-9ea2-85f2264b61f3',
    'b68c0b6c-6453-4a8e-a4b1-6c2463c13732',
    '13ab46a2-3648-40cd-91f4-91574044a063',
    '89fc944d-89f8-4ea3-9456-f50328781e43',
    '43e57e33-9cf0-41c2-aee4-7b8f9ae1c070',
    'e1fc6dcd-41d7-4a2b-8494-fb7c97949412',
    '4c737db9-8542-4686-b687-9770a5b6920f',
    '01dfae08-3ce4-4709-a308-b09deb4b6b8c',
    '680c7770-cd1c-4c21-b960-6f90ed90a448',
    '56e39fdd-2484-422f-ba05-1868a293cab9',
    '510a40df-c387-4e88-8b30-6a4933567c43',
    '607e0168-d873-447f-9ef7-95ace9a938ef',
    'abfed9aa-fcf0-4ec3-9e17-f8f8896053ce',
    '837c6346-b681-4ec3-8986-4726b42cc567',
    '39c32e6c-0901-48b8-8e55-7d273453054e',
    'fdfd7564-94a2-4419-9e8b-e30753a1e794',
    '7d67de7b-175c-4ff8-b076-7dd63bfb58b0',
    '3da11444-d5d5-4452-b3e6-c2157b267895',
    'ce1e1ea0-5bc4-4731-88ad-eaad3bfd5c4a',
    '5ddb7521-0b17-4604-a6ad-ea33671e7759',
    '359f5ada-cbf3-4f29-8772-503c76db5218',
    '789b5734-1745-4e5e-b415-8599af6034e5',
    'fd76aca8-21e0-4517-8f9f-f980997abdb2',
    '985177f1-b8ce-4c5e-bf1d-8318b48ec0c7',
    '7579154c-0320-4dde-9759-30b2c9a3a9fb',
    '97ec0e12-1b30-422f-beea-0eca82a0e8cb',
    '9b711121-aeec-4c99-8385-8df16963ac8e',
    'b48b5542-3e23-455b-a9b9-06dac8f80c2a',
    '850b95d5-bb84-4464-9ee0-98a92f9182bb',
    '5abd8042-552f-49c4-a6a2-b4083de123e5',
    'dc139dbe-9b1f-431e-9285-92edb12e2662',
    '449da602-7610-4d86-ba93-eed1b46e28c9',
    '1ac250ad-5553-437a-bc91-e1fdb7112402',
    'f539aba4-a8d9-45fe-bb50-047243111f62',
    '5b19270b-1b4f-4bab-9bb4-f45fdb3ac0a1',
    'af015203-a3d4-4ab1-9f96-2a989baf1a3d',
    'c7f918f4-e037-4496-bb2b-9e98c5a4e97f',
    'e000cd10-a5dc-40ed-91ad-401bbceea1c5',
    'd5207ed7-4329-4846-8fd5-cdf28a9eb0ea',
    '889525ed-50e2-4d48-9330-525f6cb37658',
    '2fa85786-b86b-4fdf-a025-5d89a813c2d5',
    '61aa803c-3f64-4029-b835-c1cbe6406d1b',
    '203156e7-9c93-424b-9114-aa9039d0534c',
    '486fd7d5-932f-4490-a37f-9dafb6bb0e99',
    '404c55f6-5d5e-4591-8472-8870a15f8a85',
    '2c65e308-17f6-4baa-9806-c9f2de93449e',
    'ce57cf1b-3f7a-48bb-ac06-a9afc933fb39',
    '522b9f5b-2d84-4406-b18a-b013f3ccf008',
    '0ce71a0b-587a-4ce6-897c-40b348c2ee14',
    'cec8ebf3-3c44-4e88-8682-616e0892fbc0',
    '1ee9140e-6d8e-4ffb-a621-f24b498c6624',
    'b37c55b2-1479-43a3-9c64-e1d8934f6b26',
    '68bb66c8-84fb-4bce-8f75-22e9f1722d46',
    '190c5c37-135c-483f-bf19-edfc9bf29356',
    '6364fb93-0421-45d0-aae1-f6873114d15c',
    '3e44d2fd-565a-4138-8bf4-8a86340acaac',
    '8c839652-d877-4644-a36c-ebd8b5abc8ca',
    '8a2f8a40-81c8-4959-a101-00cdd04f0b5d',
    '2ca77275-cd61-4bcf-ac28-1fa7f8230e03',
]

# create_epd_url_json(uuids)

# Test Ecoportal data
def test(uuid):
    query_string = '?format=JSON&view=extended'
    headers = {
        'Authorization': f'Bearer {ECOPORTAL_API_TOKEN}'
    }
    path = f'{ECOPORTAL_BASE_URL}/{uuid}{query_string}'
    response = requests.get(path, headers=headers)
    return response.json()
# test('94506cde-817c-4307-bef0-4a317b894e95')