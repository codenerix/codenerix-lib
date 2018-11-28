# -*- coding: utf-8 -*-
#
# django-codenerix-extensions
#
# Copyright 2017 Centrologic Computational Logistic Center S.L.
#
# Project URL : http://www.codenerix.com
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# This library is intended for encrypting as CODENERIX's Cryptography Libraries work, the basis
# for the library to work are, the KEY is always a SHA256 from your real KEY, the IV vector
# should be generated automatically on encryption time by the library and must be inserted
# at the beginning of the encrypted string (which shoul be padded with PKCS7). The full
# string IV+ENCRYPTED is encoded to Base64. For decrypting the process is the opossite, the
# raw string is decoded from Base64, the first 16 bytes are taken as the IV and the rest as
# the encrypted string, the key is hashed with SHA256 and then the encrypted string is decrypted
# using the IV and the hashed key.


import base64
import hashlib

from Cryptodome import Random
from Cryptodome.Cipher import AES


class AESCipher(object):
    """
    Adapted solution from: https://stackoverflow.com/a/21928790/1481040
    """

    def __init__(self):
        self.bs = 32

    def encrypt(self, raw, key, iv=None, b64encoded=True):
        raw = self._pad(raw)
        if iv is None:
            iv = Random.new().read(AES.block_size)
        hashkey = hashlib.sha256(key.encode()).digest()
        cipher = AES.new(hashkey, AES.MODE_CBC, iv)

        if not isinstance(raw, bytes):
            raw = raw.encode()

        if (b64encoded):
            return base64.b64encode(iv + cipher.encrypt(raw))
        else:
            return iv + cipher.encrypt(raw)

    def decrypt(self, enc, key, b64encoded=True):
        if b64encoded:
            enc = base64.b64decode(enc)
        iv = enc[:AES.block_size]
        if not isinstance(key, bytes):
            key = key.encode()
        hashkey = hashlib.sha256(key).digest()
        cipher = AES.new(hashkey, AES.MODE_CBC, iv)
        unpad = self._unpad(cipher.decrypt(enc[AES.block_size:]))
        if not isinstance(unpad, bytes):
            unpad = unpad.decode('utf-8')
        return unpad

    def _pad(self, s):
        pad = (self.bs - len(s) % self.bs) * chr(self.bs - len(s) % self.bs)
        if isinstance(s, bytes):
            pad = pad.encode()
        return s + pad

    @staticmethod
    def _unpad(s):
        return s[:-ord(s[len(s) - 1:])]
