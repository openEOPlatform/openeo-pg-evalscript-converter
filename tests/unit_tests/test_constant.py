import json

import pytest

from tests.utils import load_process_code, run_process


@pytest.fixture
def constant_process_code():
    return load_process_code("constant")


@pytest.mark.parametrize(
    "example_input,expected_output",
    [
        ({"x": 3}, 3),
        ({"x": "ABC"}, "ABC"),
        ({"x": [1, 2, 3]}, [1, 2, 3]),
        ({"x": [1, True, False, None, "String"]}, [1, True, False, None, "String"]),
        ({"x": None}, None),
        ({"x": True}, True),
        ({"x": False}, False),
        (
            {
                "x": {
                    "name": "John",
                    "surname": "Doe",
                    "age": 25,
                    "is_fake": True,
                    "hobbies": ["Sport", "Drinks", "Drugs", "Rock'n'roll"],
                }
            },
            {
                "name": "John",
                "surname": "Doe",
                "age": 25,
                "is_fake": True,
                "hobbies": ["Sport", "Drinks", "Drugs", "Rock'n'roll"],
            },
        ),
    ],
)
def test_constant(constant_process_code, example_input, expected_output):
    output = run_process(constant_process_code, "constant", example_input)
    output = json.loads(output)
    assert output == expected_output
