#!/usr/bin/env python
import os
from hashlib import sha1
import requests


SITE_ID = '8954ba2a-fa5e-447b-ada8-09c4b5ce8b29'
BASE_URL = 'https://api.netlify.com/api/v1/'
token = os.environ.get('NETLIFY_TOKEN')

def hash_file(path):
    with open(path, 'rb') as f:
        return sha1(f.read()).hexdigest()


def main():
    hash_to_path = dict()
    uri_to_hash = dict()
    hash_to_uri = dict()
    for root, dirs, files in os.walk('dist'):
        for f in files:
            full_path = os.path.join(root, f)
            hash_ = hash_file(full_path)
            hash_to_path[hash_] = full_path
            uri_to_hash[full_path.replace('dist/', '/')] = hash_
            hash_to_uri[hash_] = full_path.replace('dist/', '/')

    #post
    resp = requests.post(
        f'{BASE_URL}sites/{SITE_ID}/deploys',
        json={'files': uri_to_hash},
        headers={'Authorization': f'Bearer {token}'},
    )
    resp.raise_for_status()
    resp_data = resp.json()

    # put files
    deploy_id = resp_data['id']
    required_files = resp_data['required']
    if deploy_id is None or (not required_files):
        print('No files to upload, stopping')
        return
    else:
        print(f'{len(required_files)} files to upload:')

    for rf in required_files:
        path_to_file = hash_to_path[rf]
        uri = hash_to_uri[rf]
        print(f'Uploading {uri}...')
        with open(path_to_file, 'rb') as f:
            resp = requests.put(
                f'{BASE_URL}deploys/{deploy_id}/files{uri}',
                headers={
                    'content-type':'application/octet-stream',
                    'Authorization': f'Bearer {token}'
                },
                data=f.read(),
            )
            resp.raise_for_status()

    print('Deploy successful')


if __name__ == '__main__':
    main()
