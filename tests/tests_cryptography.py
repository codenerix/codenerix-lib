from pytest import fixture

from codenerix_lib.cryptography import AESCipher


@fixture
def raw():
    return b"Hola caracola"


@fixture
def raw_str():
    return "Hola caracola"


@fixture
def key():
    return "Adios caracol"


@fixture
def iv():
    return b"This is my IV 16"


@fixture
def encrypted():
    return b"VGhpcyBpcyBteSBJViAxNpXV4ILG6wSjn9fkwZgat06io6OfNi3daI7bmaMZT6eo"


@fixture
def encrypted_binary():
    return (
        b"This is my IV 16\x95\xd5\xe0\x82\xc6\xeb\x04\xa3\x9f"
        b"\xd7\xe4\xc1\x98\x1a\xb7N\xa2\xa3\xa3\x9f6-\xddh\x8e"
        b"\xdb\x99\xa3\x19O\xa7\xa8"
    )


def test_aes(mocker, raw, key, iv, encrypted):
    aes = AESCipher()

    class Randomizer:
        def read(self, blocksize):
            return iv

    # Mock randomizer
    mock_randomizer = mocker.patch("Cryptodome.Random.new")
    mock_randomizer.return_value = Randomizer()

    result_encrypted = aes.encrypt(raw, key)
    result_encrypted_with_iv = aes.encrypt(raw, key, iv)
    assert result_encrypted == result_encrypted_with_iv

    # Encrypt without IV
    assert result_encrypted == encrypted

    # Encrypt with IV
    assert result_encrypted_with_iv == encrypted

    # Decrypt with IV
    assert aes.decrypt(encrypted, key) == b"Hola caracola"


def test_aes_str(mocker, raw_str, key, iv, encrypted):
    aes = AESCipher()

    class Randomizer:
        def read(self, blocksize):
            return iv

    # Mock randomizer
    mock_randomizer = mocker.patch("Cryptodome.Random.new")
    mock_randomizer.return_value = Randomizer()

    result_encrypted = aes.encrypt(raw_str, key)
    result_encrypted_with_iv = aes.encrypt(raw_str, key, iv)
    assert result_encrypted == result_encrypted_with_iv

    # Encrypt without IV
    assert result_encrypted == encrypted

    # Encrypt with IV
    assert result_encrypted_with_iv == encrypted

    # Decrypt with IV
    assert aes.decrypt(encrypted, key) == b"Hola caracola"


def test_aes_binary(mocker, raw, key, iv, encrypted, encrypted_binary):
    aes = AESCipher()

    class Randomizer:
        def read(self, blocksize):
            return iv

    # Mock randomizer
    mock_randomizer = mocker.patch("Cryptodome.Random.new")
    mock_randomizer.return_value = Randomizer()

    result_encrypted = aes.encrypt(raw, key, b64encoded=False)
    result_encrypted_with_iv = aes.encrypt(raw, key, iv, b64encoded=False)
    assert result_encrypted == result_encrypted_with_iv

    # Encrypt without IV
    assert result_encrypted == encrypted_binary

    # Encrypt with IV
    assert result_encrypted_with_iv == encrypted_binary

    # Decrypt with IV
    assert (
        aes.decrypt(encrypted_binary, key, b64encoded=False)
        == b"Hola caracola"
    )
