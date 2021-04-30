### Overview

There are multiple process graphs in `tests/process_graphs`.

You can run `tests.py`. 

`gee_uc1_pol` is the UC1 process graph, which is fully valid and produces working code.
`reduce_spatial` is an artificially constructed graph which has multiple "invalid" nodes (reducing by a spatial coordinate, undefined process), so it returns the evalscripts for subgraphs.

`convert_from_process_graph(process_graph, n_output_bands=1, sample_type="AUTO", units=None, bands_dimension_name="bands", temporal_dimension_name="t")` returns a list of dicts. Each includes fields:
- evalscript: `Evalscript` object,
- invalid_node_id: id of the invalid node, input for which is the output of `evalscript`. If the graph is fully valid, `None` is returned. Not necessarily valid atm.

`Evalscript` object has a method `write` which returns a string which should be valid javascript code.
