# openEO process graph to evalscript converter
This repository contains a library for converting [openEO process graphs](https://api.openeo.org/#section/Processes/Process-Graphs) to [Sentinel Hub evalscripts](https://docs.sentinel-hub.com/api/latest/evalscript/v3/).

The motivation behind this library is to reduce the data transfer between the SH backend and the openEO backend and to move part of the processing directly to backend where the data is stored.

## API

#### convert_from_process_graph

```python
convert_from_process_graph(
    process_graph,
    n_output_bands=1,
    sample_type="FLOAT32",
    units=None,
    bands_dimension_name="bands",
    temporal_dimension_name="t"
)
```

###### Parameters

* **`process_graph`**: *dict*

    OpenEO process graph JSON as Python dict object.

* **`n_output_bands`**: *int, optional*. Default: `1`

    Number of output bands in the evalscript. This can be set if the value is known beforehand. See [docs](https://docs.sentinel-hub.com/api/latest/evalscript/v3/#output-object-properties).

* **`sample_type`**: *str, optional*. Default: `FLOAT32`

    Desired `sampleType` of the output raster. See [possible values](https://docs.sentinel-hub.com/api/latest/evalscript/v3/#sampletype).

* **`units`**: *str, optional*. Default: `None`

    Units used by all the bands in the evalscript. If `None`, `units` evalscript parameter isn't set and default units for each band are used. See [docs](https://docs.sentinel-hub.com/api/latest/evalscript/v3/#input-object-properties).

* **`bands_dimension_name`**: *str, optional*. Default: `bands`

    Name of the default dimension of type `bands` of the datacube, as set in `load_collection` and referred to in the openEO process graph.

* **`temporal_dimension_name`**: *str, optional*. Default: `t`

    Name of the default dimension of type `temporal` of the datacube, as set in `load_collection` and referred to in the openEO process graph.

* **`encode_result`**: *bool, optional*. Default: `True`

    Should the result of the evalscript be encoded with the dimensions of the data or returned as is.

###### Output

* **`evalscripts`**: *list of dicts*

    Returns a list of dicts containing the `Evalscript` objects. Every element consists of:
    - `invalid_node_id`: Id of the first invalid node after a supported subgraph. The output of the associated evalscript should be the input of the node. If it is `None`, the entire graph is valid.

    - `evalscript`: instance of and `Evalscript` object that generates an evalscript for a valid subgraph from `load_collection` to the node with id `invalid_node_id`. 


#### Evalscript

###### Constructor parameters

* **`input_bands`**: *list*

    List of bands to be imported. See [docs](https://docs.sentinel-hub.com/api/latest/evalscript/v3/#input-object-properties).

* **`nodes`**: *list*

    List of `Node` objects that constitute the valid process (sub)graph.

* **`initial_data_name`**: *str*

    The id of the initial `load_collection` node that loads the data.

* **`n_output_bands`**: *int, optional*. Default: `1`

    Number of output bands in the evalscript. This can be set if the value is known beforehand. See [docs](https://docs.sentinel-hub.com/api/latest/evalscript/v3/#output-object-properties).

* **`sample_type`**: *str, optional*. Default: `FLOAT32`

    Desired `sampleType` of the output raster. See [possible values](https://docs.sentinel-hub.com/api/latest/evalscript/v3/#sampletype).


* **`units`**: *str, optional*. Default: `None`

    Units used by all the bands in the evalscript. If `None`, `units` evalscript parameter isn't set and default units for each band are used. See [docs](https://docs.sentinel-hub.com/api/latest/evalscript/v3/#input-object-properties).

* **`mosaicking`**: *str, optional*. Default: `ORBIT`

    Works with multi-temporal data by default. See [possible values](https://docs.sentinel-hub.com/api/latest/evalscript/v3/#mosaicking).

* **`bands_dimension_name`**: *str, optional*. Default: `bands`

    Name of the default dimension of type `bands` of the datacube, as set in `load_collection` and referred to in the openEO process graph.

* **`temporal_dimension_name`**: *str, optional*. Default: `t`

    Name of the default dimension of type `temporal` of the datacube, as set in `load_collection` and referred to in the openEO process graph.

* **`datacube_definition_directory`**: *str, optional*. Default: `javascript_datacube`

    Relative path to the directory with the javascript implemetations of the processes.

* **`output_dimensions`**: *list of dicts or None, optional*. Default: `None`

    Information about the dimensions in the output datacube. This can be set if the value is known beforehand. Each element contains:
    - `name`: name of the dimension,
    - `size`: size (length) of the dimension,
    - `original_temporal`, optional: boolean, should be `True` if this is the temporal dimension generated in the initial `load_collection` node.

* **`encode_result`**: *bool, optional*. Default: `True`

    Should the result of the evalscript be encoded with the dimensions of the data or returned as is.

###### Methods

* **`write()`**:

    Returns the evalscript as a string.

* **`determine_output_dimensions()`**:

    Calculates the greatest possible dimensions of the output datacube, returning a list of dicts. Each element contains:
    - `name`: name of the dimension,
    - `size`: size (length) of the dimension,
    - `original_temporal`, optional: boolean, `True` if this is the temporal dimension generated in the initial `load_collection` node.

* **`set_output_dimensions(output_dimensions)`**:

    Setter for output dimensions. `output_dimensions` is a list of dicts. Each element contains:
    - `name`: name of the dimension,
    - `size`: size (length) of the dimension,
    - `original_temporal`, optional: boolean, should be `True` if this is the temporal dimension generated in the initial `load_collection` node.

* **`set_input_bands(input_bands)`**:

    Setter for input bands. `input_bands` is an array of strings (band names) or `None`. Output dimensions are recalculated.

* **`get_decoding_function()`**:

    Returns a `decode_data` function. The data returned by the evalscript is encoded to contain the information about the datacube dimensions and has to be decoded to obtain the actual data in a ndarray format.
    `decode_data` has the following parameters:
    - `data`: the result of processing of the associated evalscript, it should be a three-dimensional array.
    `decode_data` returns a multidimensional Python list.


#### list_supported_processes

Returns a list of process ids of supported [openEO processes](https://docs.openeo.cloud/processes).


## Workflow

1. Construct the openEO process graph

  Load a file with `json.load` or generate an openEO process graph using [openEO Python client](https://github.com/Open-EO/openeo-python-client).

2. Run the conversion

  ```python
  subgraph_evalscripts = convert_from_process_graph(process_graph)
  
  print(subgraph_evalscripts)
  >>> [{'evalscript': <pg_to_evalscript.evalscript.Evalscript object at 0x000001ABA779CA00>, 'invalid_node_id': None}]
  ```

  In this example, the entire openEO process graph could be converted to an evalscript, so we only have one entry.

3. Fetch the data

  ```python
  evalscript = subgraph_evalscripts[0]['evalscript'].write()
  print(evalscript)
  >>> "//VERSION=3 function setup(){ ..."
```
  The evalscript string can now be used to process data on Sentinel Hub. [Sentinel Hub Python client](https://sentinelhub-py.readthedocs.io/en/latest/) makes it easy to do so. 

4. Decode the fetched data

  ```python
  # Get the decoding function fo  r this evalsscript
  decoding_function = evalscript.get_decoding_function()
  # Pass the fetched data through the decoding function. 
  # The function expects a python list. If you're using Sentinel Hub Python client, the result might be a numpy array, so it has to be converted.
  decoded_data = decoding_function(fetched_data.tolist())
  print(decoded_data)
  >>> [[[1, 2, 3], [4, 5, 6], ... ]]
```


## Running notebooks

```
pipenv install --dev --pre
```

Start the notebooks

```
cd notebooks
pipenv run jupyter notebook
```

## Running tests

#### Using Docker

```
docker build -t tests .
docker run tests
```

#### Directly

Tests require a NodeJS environment. 

```
pipenv install
pipenv shell
cd tests
pytest
```

## Linting

```
pipenv run black -l 120 .
```

## Developing

Install the package in editable mode so the changes take effect immediately.
```
pipenv install -e .
```