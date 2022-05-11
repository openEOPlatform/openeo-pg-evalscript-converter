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
    assert output == expected_output

    assert output == expected_output


@pytest.mark.parametrize(
    "example_input,expected_output",
    [
        ("17:35:58Z", dict({"type": "time", "value": "1900-01-01T17:35:58.000Z"})),
        ("12:00:00Z", dict({"type": "time", "value": "1900-01-01T12:00:00.000Z"})),
        ("23:59:59Z", dict({"type": "time", "value": "1900-01-01T23:59:59.000Z"})),
        ("24:00:00Z", dict({"type": "time", "value": "1900-01-02T00:00:00.000Z"})),
        ("12:00:00.432Z", dict({"type": "time", "value": "1900-01-01T12:00:00.432Z"})),
        ("12:34:56.123Z", dict({"type": "time", "value": "1900-01-01T12:34:56.123Z"})),
        ("13:00:00+01:00", dict({"type": "time", "value": "1900-01-01T12:00:00.000Z"})),
        ("11:00:00-01:30", dict({"type": "time", "value": "1900-01-01T12:30:00.000Z"})),
        ("00:00:00+01:00", dict({"type": "time", "value": "1899-12-31T23:00:00.000Z"})),
        ("2018-01-01T12:00:00Z", dict({"type": "time", "value": "1900-01-01T12:00:00.000Z"})),
        ("2018-01-01T12:34:56.123Z", dict({"type": "time", "value": "1900-01-01T12:34:56.123Z"})),
        ("2018-01-01T13:00:00+01:00", dict({"type": "time", "value": "1900-01-01T12:00:00.000Z"})),
        ("2018-01-01T11:00:00-01:30", dict({"type": "time", "value": "1900-01-01T12:30:00.000Z"})),
        ("2018-01-01T00:00:00+01:00", dict({"type": "time", "value": "1899-12-31T23:00:00.000Z"})),
        ("2018-01-01", None),
        (None, None),
        (1, None),
        (True, None),
        ("not a temporal string", None),
        ({}, None),
        ([], None),
        ("2018-01-01T12:00:00", None),
    ],
)
def test_common_time(common_code, example_input, expected_output):
    function_name = "parse_rfc3339_time"
    output = run_javascript(
        common_code + f"process.stdout.write(JSON.stringify({function_name}({json.dumps(example_input)})))"
    )
    output = json.loads(output)

    assert output == expected_output


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


@pytest.mark.parametrize(
    "period,min_date,max_date,expected_output",
    [
        (
            "hour",
            "2020-01-05T22:19:56.000Z",
            "2020-01-06T03:42:29.000Z",
            [
                "2020-01-05T22:19:56.000Z",
                "2020-01-05T23:19:56.000Z",
                "2020-01-06T00:19:56.000Z",
                "2020-01-06T01:19:56.000Z",
                "2020-01-06T02:19:56.000Z",
                "2020-01-06T03:19:56.000Z",
            ],
        ),
        (
            "hour",
            "2020-01-05T22:19:56.000Z",
            "2020-01-06T03:12:29.000Z",
            [
                "2020-01-05T22:19:56.000Z",
                "2020-01-05T23:19:56.000Z",
                "2020-01-06T00:19:56.000Z",
                "2020-01-06T01:19:56.000Z",
                "2020-01-06T02:19:56.000Z",
            ],
        ),
        (
            "hour",
            "2020-03-25T05:23:31.000Z",
            "2020-03-25T06:23:31.000Z",
            ["2020-03-25T05:23:31.000Z", "2020-03-25T06:23:31.000Z"],
        ),
        (
            "hour",
            "2020-06-01T18:59:59.000Z",
            "2020-06-01T21:59:58.000Z",
            ["2020-06-01T18:59:59.000Z", "2020-06-01T19:59:59.000Z", "2020-06-01T20:59:59.000Z"],
        ),
        ("day", "2020-01-05T00:00:00.000Z", "2020-01-05T22:51:23.000Z", ["2020-01-05T00:00:00.000Z"]),
        (
            "day",
            "2020-01-29T00:00:00.000Z",
            "2020-02-01T00:00:00.000Z",
            [
                "2020-01-29T00:00:00.000Z",
                "2020-01-30T00:00:00.000Z",
                "2020-01-31T00:00:00.000Z",
                "2020-02-01T00:00:00.000Z",
            ],
        ),
        (
            "day",
            "2020-02-28T02:01:23.000Z",
            "2020-03-04T23:45:00.000Z",
            [
                "2020-02-28T02:01:23.000Z",
                "2020-02-29T02:01:23.000Z",
                "2020-03-01T02:01:23.000Z",
                "2020-03-02T02:01:23.000Z",
                "2020-03-03T02:01:23.000Z",
                "2020-03-04T02:01:23.000Z",
            ],
        ),
        (
            "week",
            "2020-01-05T22:19:56.000Z",
            "2020-01-25T22:19:56.000Z",
            ["2020-01-05T22:19:56.000Z", "2020-01-12T22:19:56.000Z", "2020-01-19T22:19:56.000Z"],
        ),
        (
            "week",
            "2020-03-25T05:00:00.000Z",
            "2020-04-18T04:00:00.000Z",
            [
                "2020-03-25T05:00:00.000Z",
                "2020-04-01T05:00:00.000Z",
                "2020-04-08T05:00:00.000Z",
                "2020-04-15T05:00:00.000Z",
            ],
        ),
        (
            "week",
            "2020-06-01T18:59:59.000Z",
            "2020-06-22T18:59:58.000Z",
            ["2020-06-01T18:59:59.000Z", "2020-06-08T18:59:59.000Z", "2020-06-15T18:59:59.000Z"],
        ),
        (
            "dekad",
            "2020-01-05T22:19:56.000Z",
            "2020-01-27T22:19:56.000Z",
            ["2020-01-05T22:19:56.000Z", "2020-01-15T22:19:56.000Z", "2020-01-25T22:19:56.000Z"],
        ),
        ("dekad", "2020-03-25T05:23:31.000Z", "2020-03-28T05:23:31.000Z", ["2020-03-25T05:23:31.000Z"]),
        (
            "dekad",
            "2020-06-01T18:59:59.000Z",
            "2020-07-04T18:59:59.000Z",
            [
                "2020-06-01T18:59:59.000Z",
                "2020-06-11T18:59:59.000Z",
                "2020-06-21T18:59:59.000Z",
                "2020-07-01T18:59:59.000Z",
            ],
        ),
        ("month", "2020-01-05T22:19:56.000Z", "2020-01-25T22:19:56.000Z", ["2020-01-05T22:19:56.000Z"]),
        (
            "month",
            "2020-03-25T05:23:31.000Z",
            "2020-04-27T05:23:31.000Z",
            ["2020-03-25T05:23:31.000Z", "2020-04-25T05:23:31.000Z"],
        ),
        (
            "month",
            "2020-06-01T18:59:59.000Z",
            "2020-09-11T18:59:59.000Z",
            [
                "2020-06-01T18:59:59.000Z",
                "2020-07-01T18:59:59.000Z",
                "2020-08-01T18:59:59.000Z",
                "2020-09-01T18:59:59.000Z",
            ],
        ),
        ("season", "2020-01-05T22:19:56.000Z", "2020-03-01T22:19:56.000Z", ["2020-01-05T22:19:56.000Z"]),
        (
            "season",
            "2020-03-25T05:23:31.000Z",
            "2020-11-03T05:23:31.000Z",
            ["2020-03-25T05:23:31.000Z", "2020-06-25T05:23:31.000Z", "2020-09-25T05:23:31.000Z"],
        ),
        (
            "season",
            "2020-06-01T18:59:59.000Z",
            "2020-11-23T18:59:59.000Z",
            ["2020-06-01T18:59:59.000Z", "2020-09-01T18:59:59.000Z"],
        ),
        (
            "tropical-season",
            "2020-01-05T22:19:56.000Z",
            "2022-03-24T22:19:56.000Z",
            [
                "2020-01-05T22:19:56.000Z",
                "2020-07-05T22:19:56.000Z",
                "2021-01-05T22:19:56.000Z",
                "2021-07-05T22:19:56.000Z",
                "2022-01-05T22:19:56.000Z",
            ],
        ),
        (
            "tropical-season",
            "2020-03-25T05:23:31.000Z",
            "2020-11-25T05:23:31.000Z",
            ["2020-03-25T05:23:31.000Z", "2020-09-25T05:23:31.000Z"],
        ),
        ("tropical-season", "2020-06-01T18:59:59.000Z", "2020-11-30T18:59:59.000Z", ["2020-06-01T18:59:59.000Z"]),
        ("year", "2024-06-01T18:59:59.000Z", "2024-12-31T18:59:59.000Z", ["2024-06-01T18:59:59.000Z"]),
        ("year", "2045-07-17T13:42:19.000Z", "2046-06-17T13:42:19.000Z", ["2045-07-17T13:42:19.000Z"]),
        (
            "year",
            "1945-09-23T10:05:01.000Z",
            "1947-10-23T10:05:01.000Z",
            ["1945-09-23T10:05:01.000Z", "1946-09-23T10:05:01.000Z", "1947-09-23T10:05:01.000Z"],
        ),
        ("decade", "1996-03-25T05:23:31.000Z", "2003-03-25T05:23:31.000Z", ["1996-03-25T05:23:31.000Z"]),
        (
            "decade",
            "2024-06-01T18:59:59.000Z",
            "2048-06-01T18:59:59.000Z",
            ["2024-06-01T18:59:59.000Z", "2034-06-01T18:59:59.000Z", "2044-06-01T18:59:59.000Z"],
        ),
        (
            "decade",
            "1945-09-23T10:05:01.000Z",
            "2013-01-31T10:05:01.000Z",
            [
                "1945-09-23T10:05:01.000Z",
                "1955-09-23T10:05:01.000Z",
                "1965-09-23T10:05:01.000Z",
                "1975-09-23T10:05:01.000Z",
                "1985-09-23T10:05:01.000Z",
                "1995-09-23T10:05:01.000Z",
                "2005-09-23T10:05:01.000Z",
            ],
        ),
        (
            "decade-ad",
            "1996-03-25T05:23:31.000Z",
            "2016-03-21T05:23:31.000Z",
            ["1996-03-25T05:23:31.000Z", "2006-03-25T05:23:31.000Z"],
        ),
        ("decade-ad", "2024-06-01T18:59:59.000Z", "2031-06-01T18:59:59.000Z", ["2024-06-01T18:59:59.000Z"]),
        (
            "decade-ad",
            "1945-09-23T10:05:01.000Z",
            "1973-04-21T10:05:01.000Z",
            ["1945-09-23T10:05:01.000Z", "1955-09-23T10:05:01.000Z", "1965-09-23T10:05:01.000Z"],
        ),
    ],
)
def test_date_generation(common_code, period, min_date, max_date, expected_output):
    function_name = "generateDatesInRangeByPeriod"
    output = run_javascript(
        common_code
        + f"process.stdout.write(JSON.stringify({function_name}({json.dumps(min_date)}, {json.dumps(max_date)}, {json.dumps(period)})))"
    )
    output = json.loads(output)
    assert output == expected_output


@pytest.mark.parametrize(
    "period,label,expected_output",
    [
        ("hour", "2020-01-05T22:19:56.000Z", "2020-01-05-22"),
        ("hour", "2020-03-25T05:23:31.000Z", "2020-03-25-05"),
        ("hour", "2020-06-01T18:59:59.000Z", "2020-06-01-18"),
        ("hour", "2020-07-17T13:42:19.000Z", "2020-07-17-13"),
        ("hour", "2020-09-23T10:05:01.000Z", "2020-09-23-10"),
        ("day", "2020-01-05T00:00:00.000Z", "2020-005"),
        ("day", "2020-01-29T00:00:00.000Z", "2020-029"),
        ("day", "2020-02-28T00:00:00.000Z", "2020-059"),
        ("day", "2020-07-25T00:00:00.000Z", "2020-207"),
        ("day", "2020-12-31T00:00:00.000Z", "2020-366"),
        ("day", "2021-12-31T00:00:00.000Z", "2021-365"),
        ("week", "2020-01-05T22:19:56.000Z", "2020-01"),
        ("week", "2020-03-25T05:23:31.000Z", "2020-13"),
        ("week", "2020-06-01T18:59:59.000Z", "2020-22"),
        ("week", "2020-07-17T13:42:19.000Z", "2020-29"),
        ("week", "2020-09-23T10:05:01.000Z", "2020-39"),
        ("dekad", "2020-01-05T22:19:56.000Z", "2020-01"),
        ("dekad", "2020-03-25T05:23:31.000Z", "2020-09"),
        ("dekad", "2020-06-01T18:59:59.000Z", "2020-16"),
        ("dekad", "2020-07-17T13:42:19.000Z", "2020-20"),
        ("dekad", "2020-09-23T10:05:01.000Z", "2020-27"),
        ("month", "2020-01-05T22:19:56.000Z", "2020-01"),
        ("month", "2020-03-25T05:23:31.000Z", "2020-03"),
        ("month", "2020-06-01T18:59:59.000Z", "2020-06"),
        ("month", "2020-07-17T13:42:19.000Z", "2020-07"),
        ("month", "2020-09-23T10:05:01.000Z", "2020-09"),
        ("season", "2020-01-05T22:19:56.000Z", "2020-djf"),
        ("season", "2020-03-25T05:23:31.000Z", "2020-mam"),
        ("season", "2020-06-01T18:59:59.000Z", "2020-jja"),
        ("season", "2020-07-17T13:42:19.000Z", "2020-jja"),
        ("season", "2020-09-23T10:05:01.000Z", "2020-son"),
        ("tropical-season", "2020-01-05T22:19:56.000Z", "2020-ndjfma"),
        ("tropical-season", "2020-03-25T05:23:31.000Z", "2020-ndjfma"),
        ("tropical-season", "2020-06-01T18:59:59.000Z", "2020-mjjaso"),
        ("tropical-season", "2020-07-17T13:42:19.000Z", "2020-mjjaso"),
        ("tropical-season", "2020-09-23T10:05:01.000Z", "2020-mjjaso"),
        ("year", "2005-01-05T22:19:56.000Z", "2005"),
        ("year", "1996-03-25T05:23:31.000Z", "1996"),
        ("year", "2024-06-01T18:59:59.000Z", "2024"),
        ("year", "2045-07-17T13:42:19.000Z", "2045"),
        ("year", "1945-09-23T10:05:01.000Z", "1945"),
        ("decade", "2005-01-05T22:19:56.000Z", "2000"),
        ("decade", "1996-03-25T05:23:31.000Z", "1990"),
        ("decade", "2024-06-01T18:59:59.000Z", "2020"),
        ("decade", "2045-07-17T13:42:19.000Z", "2040"),
        ("decade", "1945-09-23T10:05:01.000Z", "1940"),
        ("decade-ad", "2005-01-05T22:19:56.000Z", "2001"),
        ("decade-ad", "1996-03-25T05:23:31.000Z", "1991"),
        ("decade-ad", "2024-06-01T18:59:59.000Z", "2021"),
        ("decade-ad", "2045-07-17T13:42:19.000Z", "2041"),
        ("decade-ad", "1945-09-23T10:05:01.000Z", "1941"),
    ],
)
def test_date_formatting_by_period(common_code, period, label, expected_output):
    function_name = "formatLabelByPeriod"
    output = run_javascript(
        common_code
        + f"process.stdout.write(JSON.stringify({function_name}({json.dumps(period)}, {json.dumps(label)})))"
    )
    output = json.loads(output)
    assert output == expected_output
