### Overview

There are multiple process graphs in `tests/process_graphs`.

There are no tests atm.

You can run `test.py` in `src/pg_to_evalscript`. 

`gee_uc1_pol` is the UC1 process graph, which is fully valid and produces working code.
`reduce_spatial` is an artificially constructed graph which has multiple "invalid" nodes (reducing by a spatial coordinate, undefined process), so it returns the evalscripts for subgraphs.

`convert_from_process_graph(process_graph, n_output_bands=1, sample_type="AUTO", units=None, bands_dimension_name="bands", temporal_dimension_name="t")` returns a list of dicts. 
Each includes fields:
- evalscript: `Evalscript` object,
- invalid_node_id: id of the invalid node, input for which is the output of `evalscript`. If the graph is fully valid, `None` is returned. Not necessarily valid atm.

`Evalscript` object has a method `write` which returns a string which should be valid javascript code.

Example evalscript returned for `gee_uc1_pol`:

```
//VERSION=3
function setup() {
  return {
    input: ['VV','VH'],
    output: { bands: 1, sampleType: "AUTO" },
    mosaicking: "ORBIT"
  };
}
class DataCube {
  constructor(data, bands_dimension_name, temporal_dimension_name, fromSamples) {
    this.TEMPORAL = "temporal"
    this.BANDS = "bands"
    this.OTHER = "other"
    this.bands_dimension_name = bands_dimension_name;
    this.temporal_dimension_name = temporal_dimension_name;
    this.dimensions = [{name: this.temporal_dimension_name, labels: [], type: this.TEMPORAL}, {name: this.bands_dimension_name, labels: [], type: this.BANDS}]
    if (fromSamples) {
      this.data = this.makeArrayFromSamples(data)
    }
    else {
      this.data = data;
    }
  }

  getDimensionByName(name) {
    return this.dimensions.find(d => d.name === name)
  }

  makeArrayFromSamples(samples) {
    if (Array.isArray(samples)) {
      let newData = []
      for (let entry of samples) {
        if (this.getDimensionByName(this.bands_dimension_name).labels.length === 0) {
          this.getDimensionByName(this.bands_dimension_name).labels = Object.keys(entry)
        }
        newData.push(Object.values(entry))
      }
      return newData
    }
    else {
      if (this.getDimensionByName(this.bands_dimension_name).labels.length === 0) {
          this.getDimensionByName(this.bands_dimension_name).labels = Object.keys(samples)
        }
      return Object.values(samples)
    }
  }

  selectColumn(index) {
    return this.data.map(v => v[index])
  }

  getBandIndices(bands) {
    return bands.map(b => this.getDimensionByName(this.bands_dimension_name).labels.indexOf(b))
  }

  filterBands(bands) {
    const indices = this.getBandIndices(bands)
    if (this.dimensions.length === 1) {
      this.data = indices.map(i => this.data[i])
    }
    else {
      for(let i=0; i < this.data.length; i++) {
        this.data[i] = indices.map(ind => this.data[i][ind])
      }
    }
    this.getDimensionByName(this.bands_dimension_name).labels = bands;
  }

  removeDimension(dimension) {
    this.dimensions = this.dimensions.filter(d => d.name !== dimension)
  }

  reduceByDimension(reducer, dimension) {
    const newData = []

    if (this.dimensions.length === 1) {
      this.data.labels = this.dimensions[0].labels
      this.data = reducer({data: this.data});
      this.removeDimension(dimension)
      return
    }
    if (dimension === this.temporal_dimension_name) {
      for (let i = 0; i < this.data[0].length; i++) {
        const newValue = reducer({data: this.selectColumn(i)})
        newData.push(newValue)
      }
      this.data = newData;
      this.removeDimension(dimension)
    }
    else if (dimension === this.bands_dimension_name) {
      for (let i = 0; i < this.data.length; i++) {
        let row = this.data[i]
        row.labels = this.getDimensionByName(this.bands_dimension_name).labels
        const newValue = reducer({data: row})
        this.data[i] = newValue;
      }
      this.removeDimension(dimension)
    }
  }

  addDimensionToData(data) {
    if (!Array.isArray(data)) {
      this.data = [data]
    }
    for (let i = 0; i < data.length; i++) {
      if (Array.isArray(data[i])) {
        this.addDimensionToData(data[i])
      }
      data[i] = [data[i]]
    }
  }

  addDimension(name, label, type) {
    this.addDimensionToData(this.data)
    this.dimensions.push({name: name, labels: [label], type: type})
  }

  clone() {
    const copy = new DataCube(JSON.parse(JSON.stringify(this.data)), this.bands_dimension_name, this.temporal_dimension_name)
    copy.dimensions = JSON.parse(JSON.stringify(this.dimensions))
    return copy
  }
}


    function reduce_dimension_9a0177616c6947c39b99b893111eceab(arguments) {

        function reduce_dimension(arguments) {
            function reducer(arguments) {
    
                function mean_84393352b66e44919191008b6e88b4d4(arguments) {
                        function mean(arguments) {
                            const {data} = arguments;
                            return data.reduce((prev, curr) => prev + curr)/data.length
                        }
                    return mean(arguments)
                }

                    let mean1 = mean_84393352b66e44919191008b6e88b4d4({"data": arguments.data})
                return mean1;
            }

            const {data, dimension} = arguments; 
            const newData = data.clone()
            newData.reduceByDimension(reducer, dimension)
            return newData;
        }

        return reduce_dimension(arguments)
    }


    function filter_bands_8f5925d26f19445f9773dd4014dbb148(arguments) {
        function filter_bands(arguments) {
            const {data, bands} = arguments;
            const newData = data.clone()
            newData.filterBands(bands);
            return newData;
        }
        return filter_bands(arguments)
    }


    function filter_bands_3b78bc01985a456f89d85c1e07877c23(arguments) {
        function filter_bands(arguments) {
            const {data, bands} = arguments;
            const newData = data.clone()
            newData.filterBands(bands);
            return newData;
        }
        return filter_bands(arguments)
    }


    function reduce_dimension_90dfbddd638a400aba9ea9816ba235c1(arguments) {

        function reduce_dimension(arguments) {
            function reducer(arguments) {
    
                function array_element_76721d32b267421a8a3e5c40103395a0(arguments) {
                        function array_element(arguments) {
                            const {data, index, label} = arguments;
                            if (index !== undefined) {
                                return data[index]
                            }
                            return data[data.labels.indexOf(label)]
                        }
                    return array_element(arguments)
                }


                function array_element_dd641ac25a014d4ca32532547e4db124(arguments) {
                        function array_element(arguments) {
                            const {data, index, label} = arguments;
                            if (index !== undefined) {
                                return data[index]
                            }
                            return data[data.labels.indexOf(label)]
                        }
                    return array_element(arguments)
                }


                function subtract_b689fa4a591043db8392399972f14516(arguments) {
                        function subtract(arguments) {
                            const {x, y} = arguments;
                            return x - y
                        }
                    return subtract(arguments)
                }

                    let arrayelement1 = array_element_76721d32b267421a8a3e5c40103395a0({"data": arguments.data, "label": "VH"})
                let arrayelement2 = array_element_dd641ac25a014d4ca32532547e4db124({"data": arguments.data, "label": "VV"})
                let subtract1 = subtract_b689fa4a591043db8392399972f14516({"x": arrayelement1, "y": arrayelement2})
                return subtract1;
            }

            const {data, dimension} = arguments; 
            const newData = data.clone()
            newData.reduceByDimension(reducer, dimension)
            return newData;
        }

        return reduce_dimension(arguments)
    }


    function rename_labels_134710a5a3e046fb869d9df775a6107c(arguments) {
        function rename_labels(arguments) {
            const {data, dimension, target, source} = arguments;
            for (let i = 0; i < target.length; i++) {
                const ind = data.getDimensionByName(dimension).labels.indexOf(source[i])
                data.getDimensionByName(dimension).labels[ind] = target[i]
            }
            return data;
        }
        return rename_labels(arguments)
    }


    function rename_labels_f7d9b7c039054d7c99eca05555c01f99(arguments) {
        function rename_labels(arguments) {
            const {data, dimension, target, source} = arguments;
            for (let i = 0; i < target.length; i++) {
                const ind = data.getDimensionByName(dimension).labels.indexOf(source[i])
                data.getDimensionByName(dimension).labels[ind] = target[i]
            }
            return data;
        }
        return rename_labels(arguments)
    }


    function add_dimension_cea14d62c54647179c2b2a8f8b43101e(arguments) {
        function add_dimension(arguments) {
            const {data, name, label, type} = arguments;
            let newData = data.clone()
            newData.addDimension(name, label, type)
            return newData;
        }
        return add_dimension(arguments)
    }


    function merge_cubes_9bd19dc4e01c4d3384000a45dab520bf(arguments) {
        function merge_cubes(arguments) {
            const {cube1, cube2} = arguments;
            let overlappingDimension;

            for (let dimension of cube1.dimensions) {
                const dimension2 = cube2.getDimensionByName(dimension.name)
                if (dimension.labels.length === dimension2.labels.length && dimension.labels.every(l => dimension2.labels.includes(l))) {
                    continue;
                }
                overlappingDimension = dimension.name
                break;
            }
            const levelToMerge = cube1.dimensions.findIndex(d => d.name === overlappingDimension)
            merge(cube1.data, cube2.data, 0, levelToMerge)
            return cube1;
        }

        function merge(data1, data2, level, levelToMerge) {
            if (level === levelToMerge) {
                data1.push(...data2)
                return
            }
            level++;
            for(let i = 0; i < data1.length; i++) {
                merge(data1[i], data2[i], level, levelToMerge)
            }
        }
        return merge_cubes(arguments)
    }


    function merge_cubes_a27a2e0ae31342488cb0673c8ce4873b(arguments) {
        function merge_cubes(arguments) {
            const {cube1, cube2} = arguments;
            let overlappingDimension;

            for (let dimension of cube1.dimensions) {
                const dimension2 = cube2.getDimensionByName(dimension.name)
                if (dimension.labels.length === dimension2.labels.length && dimension.labels.every(l => dimension2.labels.includes(l))) {
                    continue;
                }
                overlappingDimension = dimension.name
                break;
            }
            const levelToMerge = cube1.dimensions.findIndex(d => d.name === overlappingDimension)
            merge(cube1.data, cube2.data, 0, levelToMerge)
            return cube1;
        }

        function merge(data1, data2, level, levelToMerge) {
            if (level === levelToMerge) {
                data1.push(...data2)
                return
            }
            level++;
            for(let i = 0; i < data1.length; i++) {
                merge(data1[i], data2[i], level, levelToMerge)
            }
        }
        return merge_cubes(arguments)
    }

function evaluatePixel(samples) {
    let loadcollection1 = new DataCube(samples, 'bands', 't', true)
        let reducedimension1 = reduce_dimension_9a0177616c6947c39b99b893111eceab({"data": loadcollection1, "dimension": "t", "reducer": {"process_graph": {"mean1": {"process_id": "mean", "arguments": {"data": {"from_parameter": "data"}}, "result": true}}}})
        let filterbands2 = filter_bands_8f5925d26f19445f9773dd4014dbb148({"bands": ["VH"], "data": reducedimension1})
        let filterbands1 = filter_bands_3b78bc01985a456f89d85c1e07877c23({"bands": ["VV"], "data": reducedimension1})
        let reducedimension2 = reduce_dimension_90dfbddd638a400aba9ea9816ba235c1({"data": reducedimension1, "dimension": "bands", "reducer": {"process_graph": {"arrayelement1": {"process_id": "array_element", "arguments": {"data": {"from_parameter": "data"}, "label": "VH"}}, "arrayelement2": {"process_id": "array_element", "arguments": {"data": {"from_parameter": "data"}, "label": "VV"}}, "subtract1": {"process_id": "subtract", "arguments": {"x": {"from_node": "arrayelement1"}, "y": {"from_node": "arrayelement2"}}, "result": true}}}})
        let renamelabels2 = rename_labels_134710a5a3e046fb869d9df775a6107c({"data": filterbands2, "dimension": "bands", "target": ["G"], "source": ["VH"]})
        let renamelabels1 = rename_labels_f7d9b7c039054d7c99eca05555c01f99({"data": filterbands1, "dimension": "bands", "target": ["R"], "source": ["VV"]})
        let adddimension1 = add_dimension_cea14d62c54647179c2b2a8f8b43101e({"data": reducedimension2, "label": "B", "name": "bands", "type": "bands"})
        let mergecubes1 = merge_cubes_9bd19dc4e01c4d3384000a45dab520bf({"cube1": renamelabels1, "cube2": renamelabels2})
        let mergecubes2 = merge_cubes_a27a2e0ae31342488cb0673c8ce4873b({"cube1": mergecubes1, "cube2": adddimension1})
    return mergecubes2.data
}
```
