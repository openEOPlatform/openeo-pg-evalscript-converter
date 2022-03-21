import json
import pytest

from tests.utils import load_script, run_javascript, run_input_validation


@pytest.fixture
def common_code():
    return load_script("../src/pg_to_evalscript/javascript_common/", "common")


@pytest.mark.parametrize(
    "example_input,expected_output",
    [
        ("2018-01-01T12:00:00Z", dict({"type": "date-time", "value": "2018-01-01T12:00:00.000Z"})),
        ("2018-01-01T12:34:56.123Z", dict({"type": "date-time", "value": "2018-01-01T12:34:56.123Z"})),
        ("2018-01-01", dict({"type": "date", "value": "2018-01-01T00:00:00.000Z"})),
        ("2018-01-01T13:00:00+01:00", dict({"type": "date-time", "value": "2018-01-01T12:00:00.000Z"})),
        ("2018-01-01T11:00:00-01:30", dict({"type": "date-time", "value": "2018-01-01T12:30:00.000Z"})),
        ("2018-01-01T00:00:00+01:00", dict({"type": "date-time", "value": "2017-12-31T23:00:00.000Z"})),
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
    output = run_javascript(
        common_code + f"process.stdout.write(JSON.stringify({function_name}({json.dumps(example_input)})))"
    )
    output = json.loads(output)


@pytest.mark.parametrize(
    "example_input,raises_exception,error_name",
    [
        # MISSING_PARAMETER
        ({"processName": "test", "parameterName": "arg1", "value": 1}, False, None),
        ({"processName": "test", "parameterName": "arg1", "value": 1, "required": True}, False, None),
        ({"processName": "test", "parameterName": "arg1", "value": 1, "required": False}, False, None),
        ({"processName": "test", "parameterName": "arg1", "required": False}, False, None),
        ({"processName": "test", "parameterName": "arg1", "required": True}, True, "MISSING_PARAMETER"),
        # WRONG_TYPE
        (
            {
                "processName": "test",
                "parameterName": "arg1",
                "value": "a",
                "required": True,
                "allowedTypes": ["string"],
            },
            False,
            None,
        ),
        (
            {"processName": "test", "parameterName": "arg1", "value": 1, "required": True, "allowedTypes": ["number"]},
            False,
            None,
        ),
        (
            {
                "processName": "test",
                "parameterName": "arg1",
                "value": "a",
                "required": True,
                "allowedTypes": ["number"],
            },
            True,
            "WRONG_TYPE",
        ),
        (
            {
                "processName": "test",
                "parameterName": "arg1",
                "value": True,
                "required": True,
                "allowedTypes": ["number", "string"],
            },
            True,
            "WRONG_TYPE",
        ),
        (
            {
                "processName": "test",
                "parameterName": "arg1",
                "value": "a",
                "required": True,
                "allowedTypes": ["string", "number"],
            },
            False,
            None,
        ),
        # NOT_NULL
        (
            {
                "processName": "test",
                "parameterName": "arg1",
                "value": None,
                "required": True,
                "nullable": True,
                "allowedTypes": ["string", "number"],
            },
            False,
            None,
        ),
        (
            {
                "processName": "test",
                "parameterName": "arg1",
                "value": None,
                "required": True,
                "nullable": False,
                "allowedTypes": ["string", "number"],
            },
            True,
            "NOT_NULL",
        ),
        # NOT_ARRAY
        (
            {"processName": "test", "parameterName": "arg1", "value": [1, 2, 3], "required": True, "array": True},
            False,
            None,
        ),
        (
            {"processName": "test", "parameterName": "arg1", "value": "[1, 2, 3]", "required": True, "array": True},
            True,
            "NOT_ARRAY",
        ),
        (
            {"processName": "test", "parameterName": "arg1", "value": "[1, 2, 3]", "required": True, "array": False},
            False,
            None,
        ),
        # NOT_INTEGER
        (
            {"processName": "test", "parameterName": "arg1", "value": 1, "required": True, "integer": True},
            False,
            None,
        ),
        (
            {"processName": "test", "parameterName": "arg1", "value": 1.2, "required": True, "integer": True},
            True,
            "NOT_INTEGER",
        ),
        (
            {"processName": "test", "parameterName": "arg1", "value": 1.2, "required": True, "integer": False},
            False,
            None,
        ),
        # check boolean
        (
            {
                "processName": "test",
                "parameterName": "arg1",
                "value": True,
                "required": True,
                "allowedTypes": ["boolean"],
            },
            False,
            None,
        ),
        (
            {
                "processName": "test",
                "parameterName": "arg1",
                "value": False,
                "required": True,
                "allowedTypes": ["boolean"],
            },
            False,
            None,
        ),
        (
            {"processName": "test", "parameterName": "arg1", "value": 0, "required": True, "allowedTypes": ["boolean"]},
            True,
            "WRONG_TYPE",
        ),
        (
            {
                "processName": "test",
                "parameterName": "arg1",
                "value": "False",
                "required": True,
                "allowedTypes": ["boolean"],
            },
            True,
            "WRONG_TYPE",
        ),
        ({"processName": "test", "parameterName": "arg1", "value": "False", "required": True}, False, None),
        (
            {
                "processName": "test",
                "parameterName": "arg1",
                "value": None,
                "required": True,
                "allowedTypes": ["boolean"],
            },
            False,
            None,
        ),
        # MIN_VALUE
        (
            {"processName": "test", "parameterName": "arg1", "value": 1, "required": True, "integer": True, "min": 0},
            False,
            None,
        ),
        (
            {"processName": "test", "parameterName": "arg1", "value": 0, "required": True, "integer": True, "min": 0},
            False,
            None,
        ),
        (
            {"processName": "test", "parameterName": "arg1", "value": -1, "required": True, "integer": True, "min": 0},
            True,
            "MIN_VALUE",
        ),
        (
            {"processName": "test", "parameterName": "arg1", "value": 1, "required": True, "integer": True, "max": 1},
            False,
            None,
        ),
        # MAX_VALUE
        (
            {"processName": "test", "parameterName": "arg1", "value": 0, "required": True, "integer": True, "max": 1},
            False,
            None,
        ),
        (
            {"processName": "test", "parameterName": "arg1", "value": 1, "required": True, "integer": True, "max": 0},
            True,
            "MAX_VALUE",
        ),
        (
            {
                "processName": "test",
                "parameterName": "arg1",
                "value": 1,
                "required": True,
                "integer": True,
                "min": 1,
                "max": 2,
            },
            False,
            None,
        ),
    ],
)
def test_validate_param(common_code, example_input, raises_exception, error_name):
    run_input_validation(common_code, "validateParameter", example_input, raises_exception, error_name)
