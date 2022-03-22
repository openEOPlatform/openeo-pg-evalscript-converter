import json

from pg_to_evalscript import convert_from_process_graph

from utils import get_process_graph_json, run_javacript


def run_benchmark(pg_name, size):
    process_graph = get_process_graph_json(pg_name)
    result = convert_from_process_graph(process_graph, encode_result=False)

    assert len(result) == 1 and result[0]["invalid_node_id"] is None

    evalscript = result[0]["evalscript"].write()
    samples = json.dumps([{"B01": 0, "B02": 1}, {"B01": 2, "B02": 3}, {"B01": 4, "B02": 5}, {"B01": None, "B02": 3}])
    test_name = f"{pg_name}".ljust(40)[:40]

    code = f"""
    {evalscript}
    console.time("{test_name}")
    for(let i=0; i < {size}; i++) {{
        evaluatePixel({samples})
    }}
    console.timeEnd("{test_name}")
    """
    print(run_javacript(code).decode("utf-8").strip())


if __name__ == "__main__":
    process_graphs = [
        "test_graph_1",
        "reduce_mean_one_band",
        "reduce_mean_one_band",
        "reduce_mean_one_band",
        "test_short_graph",
        "test_apply_absolute",
        "test_apply_math",
        "test_apply_linear_scale_range",
        "test_count_with_condition",
        "test_count_without_condition",
    ]
    dim = 1000
    size = dim ** 2
    print(f"\n{size} iterations per test ({dim}x{dim})\n")
    for process_graph in process_graphs:
        run_benchmark(process_graph, size)
