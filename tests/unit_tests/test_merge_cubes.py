import json

import pytest

from tests.utils import load_process_code, load_datacube_code, run_process


@pytest.fixture
def merge_cubes_process_code():
    return load_process_code("merge_cubes")


@pytest.mark.skip(
    "Skipping as DataCube implementation changed and this merge_cubes implementation wasn't complete/correct."
)
@pytest.mark.parametrize(
    "example_input,expected_output",
    [
        (
            {
                "cube1": {"B01": [1, 2, 3], "B02": [4, 5, 6]},
                "cube2": {"B03": [11, 12, 13], "B04": [14, 15, 16]},
            },
            {
                "BANDS": "bands",
                "OTHER": "other",
                "TEMPORAL": "temporal",
                "bands_dimension_name": "bands_name",
                "temporal_dimension_name": "temporal_name",
                "dimensions": [
                    {"labels": [], "name": "temporal_name", "type": "temporal"},
                    {"labels": ["B01", "B02", "B03", "B04"], "name": "bands_name", "type": "bands"},
                ],
                "data": [[1, 2, 3], [4, 5, 6], [11, 12, 13], [14, 15, 16]],
            },
        ),
        (
            {
                "cube1": {"B01": [1, 2, 3], "B02": [4, 5, 6]},
                "cube2": {"B02": [11, 12, 13], "B03": [14, 15, 16]},
                "overlap_resolver": "({x,y}) => x + y",
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
                "data": [[1, 2, 3], [15, 17, 19], [14, 15, 16]],
            },
        ),
        (
            {
                "cube1": {"B01": [1, 2, 3], "B02": [4, 5, 6], "B03": [7, 8, 9]},
                "cube2": {"B02": [11, 12, 13], "B03": [14, 15, 16], "B04": [42, 41, 40]},
                "overlap_resolver": "({x,y}) => x + y",
            },
            {
                "BANDS": "bands",
                "OTHER": "other",
                "TEMPORAL": "temporal",
                "bands_dimension_name": "bands_name",
                "temporal_dimension_name": "temporal_name",
                "dimensions": [
                    {"labels": [], "name": "temporal_name", "type": "temporal"},
                    {"labels": ["B01", "B02", "B03", "B04"], "name": "bands_name", "type": "bands"},
                ],
                "data": [[1, 2, 3], [15, 17, 19], [21, 23, 25], [42, 41, 40]],
            },
        ),
        (
            {
                "cube1": {"B03": [3]},
                "cube2": {"B03": [7]},
                "additional_code_specific_to_test_case": """
                    cube1.getDimensionByName(cube1.temporal_dimension_name).labels = ['01-01-2022']; 
                    cube2.getDimensionByName(cube2.temporal_dimension_name).labels = ['01-02-2022'];
                """,
            },
            {
                "BANDS": "bands",
                "OTHER": "other",
                "TEMPORAL": "temporal",
                "bands_dimension_name": "bands_name",
                "temporal_dimension_name": "temporal_name",
                "dimensions": [
                    {"labels": ["01-01-2022", "01-02-2022"], "name": "temporal_name", "type": "temporal"},
                    {"labels": ["B03"], "name": "bands_name", "type": "bands"},
                ],
                "data": [[3], [7]],
            },
        ),
    ],
)
def test_merge_cubes(merge_cubes_process_code, example_input, expected_output):
    additional_js_code_to_run = (
        load_datacube_code()
        + f"const cube1 = new DataCube({example_input['cube1']}, 'bands_name', 'temporal_name', true);"
        + f"const cube2 = new DataCube({example_input['cube2']}, 'bands_name', 'temporal_name', true);"
        + f"const overlap_resolver = eval({example_input['overlap_resolver'] if 'overlap_resolver' in example_input else ''});"
        + f"{example_input['additional_code_specific_to_test_case'] if 'additional_code_specific_to_test_case' in example_input else ''};"
    )
    process_arguments = (
        f"{{...{json.dumps(example_input)}, 'cube1': cube1, 'cube2': cube2, 'overlap_resolver': overlap_resolver}}"
    )
    output = run_process(
        merge_cubes_process_code + additional_js_code_to_run,
        "merge_cubes",
        process_arguments,
    )
    output = json.loads(output)
    assert output == expected_output


@pytest.mark.skip(
    "Skipping as DataCube implementation changed and this merge_cubes implementation wasn't complete/correct."
)
@pytest.mark.parametrize(
    "example_input,raises_exception,error_message",
    [
        (
            {
                "cube1": {"B01": [1, 2, 3], "B02": [4, 5, 6]},
                "cube2": {"B03": [11, 12, 13], "B04": [14, 15, 16]},
            },
            False,
            None,
        ),
        (
            {
                "cube1": {"B01": [1, 2, 3], "B02": [4, 5, 6]},
                "cube2": {"B02": [11, 12, 13], "B03": [14, 15, 16]},
            },
            True,
            "Overlapping data cubes, but no overlap resolver has been specified.",
        ),
    ],
)
def test_merge_cubes_exceptions(merge_cubes_process_code, example_input, raises_exception, error_message):
    additional_js_code_to_run = (
        load_datacube_code()
        + f"const cube1 = new DataCube({example_input['cube1']}, 'bands_name', 'temporal_name', true);"
        + f"const cube2 = new DataCube({example_input['cube2']}, 'bands_name', 'temporal_name', true);"
        + f"const overlap_resolver = eval({example_input['overlap_resolver'] if 'overlap_resolver' in example_input else ''});"
    )
    process_arguments = (
        f"{{...{json.dumps(example_input)}, 'cube1': cube1, 'cube2': cube2, 'overlap_resolver': overlap_resolver}}"
    )
    if raises_exception:
        with pytest.raises(Exception) as exc:
            run_process(
                merge_cubes_process_code + additional_js_code_to_run,
                "merge_cubes",
                process_arguments,
            )
        assert error_message in str(exc.value)

    else:
        run_process(
            merge_cubes_process_code + additional_js_code_to_run,
            "merge_cubes",
            process_arguments,
        )
