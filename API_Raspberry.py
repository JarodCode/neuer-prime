# stdlib imports
import json
import time
import requests


# base url for all requests
# Think about modifying the URL to use Raspberry IP address and Raspberry open port
BASE_URL = "http://10.111.4.33:3000"
# Something like: "http://192.168.12.83:3000"


class DweepyError(Exception):
    pass


def _request(method, url, session=None, **kwargs):
    """Make HTTP request, raising an exception if it fails.
    """
    url = BASE_URL + url

    if session:
        request_func = getattr(session, method)
    else:
        request_func = getattr(requests, method)
    response = request_func(url, **kwargs)
    # raise an exception if request is not successful
    if not response.status_code == requests.codes.ok:
        raise DweepyError('HTTP {0} response'.format(response.status_code))
    response_json = response.json()
    if "this" in response_json: # Original Dweet method
        if response_json['this'] == 'failed':
            raise DweepyError(response_json['because'])
        return response_json['with']
    else: # Our server method
        return response_json["response"]


def _send_dweet(payload, url, params=None, session=None):
    """Send a dweet to dweet.io
    """
    data = json.dumps(payload)
    headers = {'Content-type': 'application/json'}
    return _request('post', url, data=data, headers=headers, params=params, session=session)


def dweet_for(thing_name, payload, key=None, session=None):
    """Send a dweet to dweet.io for a thing with a known name
    """
    if key is not None:
        params = {'key': key}
    else:
        params = None
    return _send_dweet(payload, '/dweet/for/{0}'.format(thing_name), params=params, session=session)

def dweet_multiple_for(thing_name, payload, key=None, session=None):
    """Send a dweet to dweet.io for a thing with a known name
    """
    if key is not None:
        params = {'key': key}
    else:
        params = None
    return _send_dweet(payload, '/dweet/multiple/for/{0}'.format(thing_name), params=params, session=session)

def get_dweets_for(thing_name):
    """Get all the dweets for a dweeter
    """
    res = _request('get', '/get/dweets/for/{0}'.format(thing_name), params=None, session=None)["dweets"]
    return [{**r, "content": json.loads(r["content"])} for r in res]

def get_data(data):
    return [(item['content']['name'], item['content']['score']) for item in data]

def get_latest_dweet_for(thing_name, key=None, session=None):
    """Read the latest dweet for a dweeter
    """
    if key is not None:
        params = {'key': key}
    else:
        params = None
    return _request('get', '/get/latest/dweet/for/{0}'.format(thing_name), params=params, session=session)


def delete_all_dweets_for(thing_name):
    """Delete all the dweets for a dweeter
    """
    return _request('delete', '/delete/dweets/for/{0}'.format(thing_name), params=None, session=None)




def main():
    def test_post_single_dweet():
        thing_name = "testThing"
        payload = {"temperature": 22, "humidity": 50}
        try:
            response = dweet_for(thing_name, payload)
            print("POST single dweet response:", response)
        except Exception as e:
            print("Failed to POST single dweet:", e)

    def test_post_multiple_dweets():
        thing_name = "testThing"
        payloads = [{"temperature": 22, "humidity": 50}, {"temperature": 23, "humidity": 55}]
        try:
            response = dweet_multiple_for(thing_name, payloads)
            print("POST multiple dweets response:", response)
        except Exception as e:
            print("Failed to POST multiple dweets:", e)

    def test_get_dweets():
        thing_name = "testThing"
        try:
            response = get_dweets_for(thing_name)
            print("GET dweets response:", response)
        except Exception as e:
            print("Failed to GET dweets:", e)

    def test_get_latest_dweet():
        thing_name = "testThing"
        try:
            response = get_latest_dweet_for(thing_name)
            print("GET latest dweet response:", response)
        except Exception as e:
            print("Failed to GET latest dweet:", e)

    def test_delete_dweets():
        thing_name = "testThing"
        try:
            response = delete_all_dweets_for(thing_name)
            print("DELETE all dweets response:", response)
        except Exception as e:
            print("Failed to DELETE dweets:", e)

    def test_upload_file(remote_filename, local_filename):
        files = {'file': (remote_filename, open(local_filename, 'rb'))}  # Open file in binary-read mode
        try:
            response = requests.post(BASE_URL + "/data/upload-file", files=files)
            print("POST upload file response:", response.json())
        except Exception as e:
            print("Failed to upload file:", e)
        finally:
            files['file'][1].close()  # Close the file after the upload

    def test_display_text():
        try:
            response = requests.post(BASE_URL + "/display-text",
                                     json={"R": 255, "G": 255, "B": 255, "text": "Hello, world!"})
            print("Display text response:", response.json())
        except Exception as e:
            print("Failed to display text:", e)

    def test_play_sound(sound_path):
        try:
            response = requests.post(BASE_URL + "/play-sound", json={"sound_path": sound_path})
            print("Play sound response:", response.json())
            return response.json().get('pid')
        except Exception as e:
            print("Failed to play sound:", e)
            return None

    def test_stop_sound(pid):
        if pid:
            try:
                response = requests.post(BASE_URL + "/stop-sound", json={"pid": pid})
                print("Stop sound response:", response.json())
            except Exception as e:
                print("Failed to stop sound:", e)

    test_post_single_dweet()
    test_post_multiple_dweets()
    time.sleep(1)  # Adding a short delay to allow the data to be processed on the server
    test_get_dweets()
    test_get_latest_dweet()
    test_delete_dweets()
    test_upload_file("hello_world.txt", "Hello World!")
    test_display_text()

    music_file = "path_to_a_music_file.mp3"
    test_upload_file("music.mp3", music_file)
    # Sound functionality tests
    PID = test_play_sound("music.mp3")
    time.sleep(2)  # Play music for 2 seconds
    test_stop_sound(PID)


if __name__ == "__main__":
    main()
