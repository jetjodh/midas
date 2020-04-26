import requests

files = {'upload_file': open('text.txt', 'rb')}
r = requests.post('http://127.0.0.1:5000/automated_testing', files=files)
print (r.text)   