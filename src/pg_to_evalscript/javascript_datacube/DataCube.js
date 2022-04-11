class DataCube {
    // data: SH samples or an ndarray
    // bands_dimension_name: name  to use for the default bands dimension
    // temporal_dimension_name: name to use for the default temporal dimension
    // fromSamples: boolean, if true `data` is expected to be in format as argument `samples` passed to `evaluatePixel` in an evalscript, else ndarray
    constructor(data, bands_dimension_name, temporal_dimension_name, fromSamples, bands_metadata) {
        this.TEMPORAL = "temporal"
        this.BANDS = "bands"
        this.OTHER = "other"
        this.bands_dimension_name = bands_dimension_name;
        this.temporal_dimension_name = temporal_dimension_name;
        this.dimensions = [{
            name: this.temporal_dimension_name,
            labels: [],
            type: this.TEMPORAL
        }, {
            name: this.bands_dimension_name,
            labels: [],
            type: this.BANDS
        }]
        if (fromSamples) {
            this.data = this.makeArrayFromSamples(data)
        } else {
            this.data = data;
        }
        this.bands_metadata = bands_metadata
    }

    getDimensionByName(name) {
        return this.dimensions.find(d => d.name === name)
    }

    // Converts `samples` object to ndarray of shape [number of samples, number of bands]
    // `samples` is eqivalent to the first argument of `evaluatePixel` method in an evalscript
    // Either object or array of objects (non-temporal and temporal scripts respectively)
    makeArrayFromSamples(samples) {
        if (Array.isArray(samples)) {
            if (samples.length === 0) {
                return ndarray([], [0, 0])
            }
            this._setDimensionLabelsIfEmpty(this.bands_dimension_name, Object.keys(samples[0]))
            let newData = []
            for (let entry of samples) {
                newData = newData.concat(extractValues(entry))
            }
            return ndarray(newData, [samples.length, extractValues(samples[0]).length])
        } else {
            this._setDimensionLabelsIfEmpty(this.bands_dimension_name, Object.keys(samples))
            const newData = Object.values(samples)
            return ndarray(newData, [1, newData.length])
        }
    }

    _setDimensionLabelsIfEmpty(dimension, labels) {
        if (this.getDimensionByName(dimension).labels.length === 0) {
            this.getDimensionByName(dimension).labels = labels
        }
    }

    getBandIndices(bands) {
        const bandsLabels = this.getDimensionByName(this.bands_dimension_name).labels
        const indices = []
        for (let band of bands) {
            const ind = bandsLabels.indexOf(band)
            if (ind !== -1) {
                indices.push(ind)
            }
        }
        return indices
    }

    getBand(name) {
        let bandToReturn = null
        for (let band of this.bands_metadata) {
            if (band.common_name === name) {
                bandToReturn = band;
            }

            if (band.name === name) {
                bandToReturn = band;
                break;
            }
        }

        return bandToReturn;
    }

    filterBands(bands) {
        const indices = this.getBandIndices(bands);
        const axis = this.dimensions.findIndex((e) => e.name === this.bands_dimension_name);
        this._filter(axis, indices);
        this.getDimensionByName(this.bands_dimension_name).labels =
            this.getDimensionByName(this.bands_dimension_name).labels.filter((lab) =>
                bands.includes(lab)
            );
    }

    removeDimension(dimension) {
        const idx = this.dimensions.findIndex(d => d.name === dimension);
        this.dimensions = this.dimensions.filter(d => d.name !== dimension);
        const newDataShape = this.data.shape;
        newDataShape.splice(idx, 1);
        this.data = ndarray(this.data.data, newDataShape)
    }

    addDimension(name, label, type) {
        this._addDimension(0)
        this.dimensions.unshift({
            name: name,
            labels: [label],
            type: type
        })
    }

    extendFinalDimensionWithData(axis, dataToAdd) {
        const finalShape = this.getDataShape()
        finalShape[axis]++;
        
        const finalData = this.insertIntoFinalDimension(dataToAdd, finalShape[axis], finalShape[axis] - 1)     
        this.data = ndarray(finalData, finalShape)
    }

    insertIntoFinalDimension(dataToAdd, dimensionSize, locationInDimension) {
        const dataArr = this.data.data;
        for (let i = 0; i < dataToAdd.length; i++) {
            dataArr.splice(
                i * dimensionSize + locationInDimension, 
                0, 
                dataToAdd[i]
            );
        }

        return dataArr;
    }

    clone() {
        const copy = new DataCube(ndarray(this.data.data.slice(), this.data.shape), this.bands_dimension_name, this.temporal_dimension_name)
        const newDimensions = []
        for (let dim of this.dimensions) {
            newDimensions.push({
                name: dim.name,
                labels: dim.labels.slice(),
                type: dim.type
            })
        }
        copy.dimensions = newDimensions
        return copy
    }

    flattenToArray() {
        if ((!this.data.shape || this.data.shape.length === 0) && this.data.data.length === 1) {
            // We have a scalar.
            return this.data.data[0]
        }
        return flattenToNativeArray(this.data)
    }

    encodeData() {
        const shape = this.getDataShape();
        const flattenedData = this.flattenToArray();
        return [...shape, ...flattenedData];
    }

    // reducer: function, accepts `data` (labeled array) and `context` (any)
    // dimension: string, name of one of the existing dimensions
    reduceByDimension(reducer, dimension, context) {
        const data = this.data
        const axis = this.dimensions.findIndex(e => e.name === dimension)
        const labels = this.dimensions[axis].labels
        const allCoords = this._iterateCoords(data.shape.slice(), [axis]) // get the generator, axis of the selected dimension is `null` (entire dimension is selected)
        const newValues = []

        for (let coord of allCoords) {
            const dataToReduce = convert_to_1d_array(data.pick.apply(data, coord)) // Convert selection to a native array
            dataToReduce.labels = labels // Add dimension labels to array
            const newVals = reducer({
                data: dataToReduce,
                context: context
            })
            newValues.push(newVals)
        }

        const newShape = data.shape.slice()
        newShape.splice(axis, 1) // The selected dimension is removed
        this.data = ndarray(newValues, newShape)
        this.dimensions.splice(axis, 1) // Remove dimension information
    }

    getDataShape() {
        return this.data.shape;
    }

    _addDimension(axis) {
        // new dimension is added before the axis
        this.data.shape.splice(axis, 0, 1)
        this.data = ndarray(this.data.data, this.data.shape)
    }

    // axis: integer, index of the dimension to filter
    // coordArr: array of indices of the dimension to keep
    _filter(axis, coordArr) {
        const length = this.data.data.length
        const stride = this.data.stride[axis]
        const axisSize = this.data.shape[axis]
        const newData = []

        for (let i = 0; i < length; i++) {
            if (coordArr.includes(Math.floor(i / stride) % axisSize)) {
                newData.push(this.data.data[i])
            }
        }

        const newShape = this.data.shape
        newShape[axis] = coordArr.length
        this.data = ndarray(newData, newShape)
    }

    // process: function, accepts `data` (labeled array) and `context` (any)
    apply(process, context) {
        const allCoords = this._iterateCoords(this.data.shape)
        for (let coords of allCoords) {
            this.data.set(...coords, process({
                "x": this.data.get.apply(this.data, coords),
                context: context
            }))
        }
    }

    // Generator that visits all coordinates of array with `shape`, keeping nullAxes `null`
    // shape: sizes of dimensions
    // nullAxes: array with axes that should be kept null
    * _iterateCoords(shape, nullAxes = []) {
        const cumulatives = fill(shape.slice(), 0);
        const coords = shape.slice();
        for (let axis of nullAxes) {
            shape[axis] = 1
            coords[axis] = null
        }
        let total = 1;
        for (let d = shape.length - 1; d >= 0; d--) {
            cumulatives[d] = total;
            total *= shape[d];
        }
        for (let i = 0; i < total; i++) {
            for (let d = shape.length - 1; d >= 0; d--) {
                if (coords[d] === null) {
                    continue
                }
                coords[d] = Math.floor(i / cumulatives[d]) % shape[d];
            }
            yield coords
        }
    }
}