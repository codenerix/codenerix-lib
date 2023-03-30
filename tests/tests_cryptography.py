from pytest import fixture

from codenerix_lib.cryptography import AESCipher


@fixture
def raw():
    return b"Hola caracola"


@fixture
def key():
    return "Adios caracol"


@fixture
def iv():
    return b"This is my IV 16"


@fixture
def encrypted():
    return b"VGhpcyBpcyBteSBJViAxNpXV4ILG6wSjn9fkwZgat06io6OfNi3daI7bmaMZT6eo"


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
