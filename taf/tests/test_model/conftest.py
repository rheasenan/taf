import json
from pathlib import Path

from taf.tests.conftest import TEST_DATA_PATH

from pytest import fixture


REPOSITORY_DESCRIPTION_INPUT_DIR = TEST_DATA_PATH / "repository_description_inputs"
NO_DELEGATIONS_INPUT = REPOSITORY_DESCRIPTION_INPUT_DIR / "no_delegations.json"
NO_YUBIKEYS_INPUT = REPOSITORY_DESCRIPTION_INPUT_DIR / "no_yubikeys.json"
WITH_DELEGATIONS_INPUT = REPOSITORY_DESCRIPTION_INPUT_DIR / "with_delegations.json"
INVALID_PUBLIC_KEY_INPUT = REPOSITORY_DESCRIPTION_INPUT_DIR / "invalid_public_key.json"
INVALID_KEYS_NUMBER_INPUT = (
    REPOSITORY_DESCRIPTION_INPUT_DIR / "invalid_keys_number.json"
)
INVALID_PATH_INPUT = REPOSITORY_DESCRIPTION_INPUT_DIR / "invalid_path.json"
OLD_YUBIKEY_INPUT = REPOSITORY_DESCRIPTION_INPUT_DIR / "with_old_yubikey.json"


def _read_json(path):
    return json.loads(Path(path).read_text())


@fixture
def no_delegations_json_input():
    return _read_json(NO_DELEGATIONS_INPUT)


@fixture
def no_yubikeys_json_input():
    return _read_json(NO_YUBIKEYS_INPUT)


@fixture
def with_delegations_json_input():
    return _read_json(WITH_DELEGATIONS_INPUT)


@fixture
def invalid_public_key_json_input():
    return _read_json(INVALID_PUBLIC_KEY_INPUT)


@fixture
def invalid_keys_number_json_input():
    return _read_json(INVALID_KEYS_NUMBER_INPUT)


@fixture
def invalid_path_input():
    return _read_json(INVALID_PATH_INPUT)


@fixture
def with_old_yubikey():
    return _read_json(OLD_YUBIKEY_INPUT)