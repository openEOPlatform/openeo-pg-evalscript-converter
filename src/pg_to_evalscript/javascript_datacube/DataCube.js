class DataCube {
    constructor(data, bands_dimension_name, temporal_dimension_name, fromSamples) {
        // data: SH samples or an ndarray
        // bands_dimension_name: name  to use for the default bands dimension
        // temporal_dimension_name: name to use for the default temporal dimension
        // fromSamples: boolean, if true `data` is expected to be in format as argument `samples` passed to `evaluatePixel` in an evalscript, else ndarray
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
    }

    getDimensionByName(name) {
        return this.dimensions.find(d => d.name === name)
    }

    makeArrayFromSamples(samples) {
        // Converts `samples` object to ndarray of shape [number of samples, number of bands]
        // `samples` is eqivalent to the first argument of `evaluatePixel` method in an evalscript
        // Either object or array of objects (non-temporal and temporal scripts respectively)
        if (Array.isArray(samples)) {
            if (samples.length === 0) {
                return ndarray([])
            }
            if (this.getDimensionByName(this.bands_dimension_name).labels.length === 0) {
                this.getDimensionByName(this.bands_dimension_name).labels = Object.keys(samples[0]) // Sets bands names as bands dimension labels
            }
            let newData = []
            for (let entry of samples) {
                newData = newData.concat(extractValues(entry))
            }
            return ndarray(newData, [samples.length, extractValues(samples[0]).length])
        } else {
            if (this.getDimensionByName(this.bands_dimension_name).labels.length === 0) {
                this.getDimensionByName(this.bands_dimension_name).labels = Object.keys(samples)
            }
            const newData = Object.values(samples)
            return ndarray(newData, [1, newData.length])
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
        return flattenToNativeArray(this.data)
    }

    encodeData() {
        const shape = this.getDataShape();
        const flattenedData = this.flattenToArray();
        return [...shape, ...flattenedData];
    }

    reduceByDimension(reducer, dimension, context) {
        // reducer: function, accepts `data` (labeled array) and `context` (any)
        // dimension: string, name of one of the existing dimensions
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

    _filter(dim, coordArr) {
        const shape = this.data.shape
        const length = this.data.data.length
        const stepSlice = shape.slice(dim)
        shape[dim] = coordArr.length
        const newData = []
        let step = 1

        for (let s of stepSlice) {
            step *= s
        }

        for (let i = 0; i < length; i++) {
            if (coordArr.includes(i % step)) {
                newData.push(this.data.data[i])
            }
        }
        this.data = ndarray(newData, shape)
    }

    apply(process, context) {
        if (isNotSubarray(this.data, this.data.shape)) {
            const newData = []
            const length = this.data.data.length
            for (let i = 0; i < length; i++) {
                newData.push(process({
                    "x": this.data.data[i],
                    context: context
                }))
            }
            this.data.data = newData
        } else {
            const shape = this.data.shape
            const cumulatives = fill(shape.slice(), 0);
            const coords = shape.slice();
            let total = 1;

            for (let d = shape.length - 1; d >= 0; d--) {
                cumulatives[d] = total;
                total *= shape[d];
            }
            for (let i = 0; i < total; i++) {
                for (let d = shape.length - 1; d >= 0; d--) {
                    coords[d] = Math.floor(i / cumulatives[d]) % shape[d];
                }
                const args = coords.concat([process({
                    "x": this.data.get.apply(this.data, coords),
                    context: context
                })])
                this.data.set.apply(this.data, args)
            }
        }
    }

    * _iterateCoords(shape, nullAxes) {
        // Generator that visits all coordinates of array with `shape`, keeping nullAxes `null`
        // shape: sizes of dimensions
        // nullAxes: array with axes that should be kept null
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