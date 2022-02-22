import json

import pytest

from tests.utils import load_script, run_javacript


@pytest.fixture
def common_code():
    return load_script("../src/pg_to_evalscript/javascript_common/", "common")


@pytest.mark.parametrize(
    "example_input,expected_output",
    [
        ("2018-01-01T12:00:00Z", "2018-01-01T12:00:00.000Z"),
        ("2018-01-01T12:34:56.123Z", "2018-01-01T12:34:56.123Z"),
        ("2018-01-01", "2018-01-01T00:00:00.000Z"),
        ("2018-01-01T13:00:00+01:00", "2018-01-01T12:00:00.000Z"),
        ("2018-01-01T11:00:00-01:30", "2018-01-01T12:30:00.000Z"),
        ("2018-01-01T00:00:00+01:00", "2017-12-31T23:00:00.000Z"),
        (None, None),
        (1, None),
        (True, None),
        ("not a temporal string", None),
        ({}, None),
        ([], None),
        ("2018-01-01T12:00:00", None),
    ],
)
def test_common(common_code, example_input, expected_output):
    function_name = "parse_rfc3339"
    output = run_javacript(
        common_code + f"process.stdout.write(JSON.stringify({function_name}({json.dumps(example_input)})))"
    )
    output = json.loads(output)
    assert output == expected_output
