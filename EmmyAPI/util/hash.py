#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import base64
import hashlib


def create_auth_string(username, password, keys):
    hashed = hash_sha1(password, pepper=keys[0])
    hashed = hash_sha1(hashed, pepper=keys[1])
    hashed = hash_sha1(hashed, pepper=keys[2])
    hashed = hash_sha1(hashed, pepper=keys[3] + username)
    b64 = base64.b64encode('{}:{}'.format(username, hashed).encode())
    return 'Basic {}'.format(b64.decode())


def hash_sha1(message, pepper=''):
    hash_object = hashlib.sha1((pepper + message).encode())
    return hash_object.hexdigest()
