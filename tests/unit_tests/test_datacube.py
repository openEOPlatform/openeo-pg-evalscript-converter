import json

import pytest

from tests.utils import load_datacube_code, with_stdout_call, run_javascript


@pytest.fixture
def datacube_code():
    def wrapped(samples):
        return load_datacube_code() + f"\nconst datacube = new DataCube({json.dumps(samples)}, 'b', 't', true)"

    return wrapped


@pytest.mark.parametrize(
    "example_samples,expected_data,expected_shape",
    [
        ([{"B01": 1, "B02": 2}, {"B01": 3, "B02": 4}], [1, 2, 3, 4], [2, 2]),
        ({"B01": 1, "B02": 2}, [1, 2], [1, 2]),
        ([{"B01": 1, "B02": 2, "B03": 3, "B04": 4}], [1, 2, 3, 4], [1, 4]),
    ],
)
def test_makeArrayFromSamples(datacube_code, example_samples, expected_data, expected_shape):
    testing_code = datacube_code(example_samples) + with_stdout_call("datacube")
    output = run_javascript(testing_code)
    output = json.loads(output)
    assert output["data"]["data"] == expected_data
    assert output["data"]["shape"] == expected_shape
