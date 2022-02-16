import json

import pytest

from tests.utils import load_process_code, run_process_with_additional_js_code


@pytest.fixture
def merge_cubes_process_code():
    return load_process_code("merge_cubes")


@pytest.mark.parametrize(
    "example_input,expected_output",
    [
        (
            {
                "cube1": {"B01": [1, 2, 3], "B02": [4, 5, 6], "B03": [7, 8, 9]},
                "cube2": {"B01": [11, 12, 13], "B02": [14, 15, 16], "B03": [17, 18, 19]},
            },
            {
                "BANDS": "bands",
                "OTHER": "other",
                "TEMPORAL": "temporal",
                "bands_dimension_name": "bands_name",
                "temporal_dimension_name": "temporal_name",
                "dimensions": [
                    {"labels": [], "name": "temporal_name", "type": "temporal"},
                    {"labels": ["B01", "B02", "B03"], "name": "bands_name", "type": "bands"},
                ],
                "data": [[1, 2, 3], [4, 5, 6], [7, 8, 9]],
            },
        ),
        (
            {
                "cube1": {"B01": [1, 2, 3], "B02": [4, 5, 6], "B03": [7, 8, 9]},
                "cube2": {"B04": [11, 12, 13], "B05": [14, 15, 16], "B06": [17, 18, 19]},
                "overlap_resolver": "({x,y}) => { if ((x*3) >= y) { return x; } return y; }",
            },
            {
                "BANDS": "bands",
                "OTHER": "other",
                "TEMPORAL": "temporal",
                "bands_dimension_name": "bands_name",
                "temporal_dimension_name": "temporal_name",
                "dimensions": [
                    {"labels": [], "name": "temporal_name", "type": "temporal"},
                    {"labels": ["B01", "B02", "B03"], "name": "bands_name", "type": "bands"},
                ],
                "data": [[11, 12, 13], [14, 5, 6], [7, 8, 9]],
            },
        ),
        (
            {
                "cube1": {"B01": [1, 2, 3], "B02": [4, 5, 6], "B03": [7, 8, 9]},
                "cube2": {"B04": [11, 12, 13], "B05": [14, 15, 16], "B06": [17, 18, 19]},
                "overlap_resolver": "({x,y}) => { return y; }",
            },
            {
                "BANDS": "bands",
                "OTHER": "other",
                "TEMPORAL": "temporal",
                "bands_dimension_name": "bands_name",
                "temporal_dimension_name": "temporal_name",
                "dimensions": [
                    {"labels": [], "name": "temporal_name", "type": "temporal"},
                    {"labels": ["B01", "B02", "B03"], "name": "bands_name", "type": "bands"},
                ],
                "data": [[11, 12, 13], [14, 15, 16], [17, 18, 19]],
            },
        ),
    ],
)
def test_merge_cubes(merge_cubes_process_code, example_input, expected_output):
    additional_js_code_to_run = (
        f"const cube1 = new DataCube({example_input['cube1']}, 'bands_name', 'temporal_name', true);"
        + f"const cube2 = new DataCube({example_input['cube2']}, 'bands_name', 'temporal_name', true);"
        + f"const overlap_resolver = eval({example_input['overlap_resolver'] if 'overlap_resolver' in example_input else ''});"
    )
    output = run_process_with_additional_js_code(
        merge_cubes_process_code,
        "merge_cubes",
        example_input,
        True,
        additional_js_code_to_run,
        additional_params_in_string="'cube1': cube1, 'cube2': cube2, 'overlap_resolver': overlap_resolver",
    )
    output = json.loads(output)
    assert output == expected_output


@pytest.mark.parametrize(
    "example_input,raises_exception,error_message",
    [
        (
            {
                "cube1": {"B01": [1, 2, 3], "B02": [4, 5, 6], "B03": [7, 8, 9]},
                "cube2": {"B04": [11, 12, 13], "B05": [14, 15, 16], "B06": [17, 18, 19]},
            },
            True,
            "Overlapping data cubes, but no overlap resolver has been specified.",
        ),
        (
            {
                "cube1": {"B01": [1, 2, 3], "B02": [4, 5, 6], "B03": [7, 8, 9]},
                "cube2": {"B01": [11, 12, 13], "B02": [14, 15, 16], "B03": [17, 18, 19]},
            },
            False,
            None,
        ),
    ],
)
def test_merge_cubes_exceptions(merge_cubes_process_code, example_input, raises_exception, error_message):
    additional_js_code_to_run = (
        f"const cube1 = new DataCube({example_input['cube1']}, 'bands_name', 'temporal_name', true);"
        + f"const cube2 = new DataCube({example_input['cube2']}, 'bands_name', 'temporal_name', true);"
        + f"const overlap_resolver = eval({example_input['overlap_resolver'] if 'overlap_resolver' in example_input else ''});"
    )
    if raises_exception:
        with pytest.raises(Exception) as exc:
            run_process_with_additional_js_code(
                merge_cubes_process_code,
                "merge_cubes",
                example_input,
                True,
                additional_js_code_to_run,
                additional_params_in_string="'cube1': cube1, 'cube2': cube2, 'overlap_resolver': overlap_resolver",
            )
        assert error_message in str(exc.value)

    else:
        run_process_with_additional_js_code(
            merge_cubes_process_code,
            "merge_cubes",
            example_input,
            True,
            additional_js_code_to_run,
            additional_params_in_string="'cube1': cube1, 'cube2': cube2, 'overlap_resolver': overlap_resolver",
        )
