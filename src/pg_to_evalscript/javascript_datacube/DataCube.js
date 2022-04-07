class DataCube {
    // data: SH samples or an ndarray
    // bands_dimension_name: name  to use for the default bands dimension
    // temporal_dimension_name: name to use for the default temporal dimension
    // fromSamples: boolean, if true `data` is expected to be in format as argument `samples` passed to `evaluatePixel` in an evalscript, else ndarray
    constructor(data, bands_dimension_name, temporal_dimension_name, fromSamples, scenes) {
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
        if (scenes) {
            let dates = [];
            for (let scene of scenes) {
                dates.push(scene.date);
            }
            this.setDimensionLabels(this.temporal_dimension_name, dates);
        }
    }

    getDimensionByName(name) {
        return this.dimensions.find(d => d.name === name)
    }

    getTemporalDimensions() {
        const temporalDimensions = this.dimensions.filter(d => d.type === this.TEMPORAL);

        if (temporalDimensions.length === 0) {
            throw new Error("No temporal dimension found.");
        }

        return temporalDimensions;
    }

    setDimensionLabels(dimension, labels) {
        for (let dim of this.dimensions) {
            if (dim.name === dimension) {
                dim.labels = labels
            }
        }
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

    getFilteredTemporalIndices(temporalDimension, start, end) {
        const temporalLabels = this.getDimensionByName(temporalDimension).labels;
        const indices = [];
        for (let i = 0; i < temporalLabels.length; i++) {
            const date = parse_rfc3339(temporalLabels[i]);
            if (!date) {
                throw new Error("Invalid ISO date string in temporal dimension label.");
            }

            if ((start === null || date.value >= start.value) && (end === null || date.value < end.value)) {
                indices.push(i);
            }
        }
        return indices;
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

    filterTemporal(extent, dimensionName) {
        if (dimensionName) {
            const dimension = this.getDimensionByName(dimensionName);

            if (dimension === undefined) {
                throw new Error(`Dimension not available.`);
            }

            if (dimension.type !== this.TEMPORAL) {
                throw new Error(`Dimension is not of type temporal.`);
            }

            this._filterTemporalByDimension(extent, dimension);

        } else {
            const dimensions = this.getTemporalDimensions();
            for (let dimension of dimensions) {
                this._filterTemporalByDimension(extent, dimension);
            }
        }
    }

    _filterTemporalByDimension(extent, dimension) {
        const axis = this.dimensions.findIndex((e) => e.name === dimension.name);
        const temporalLabels = dimension.labels;

        const parsedExtent = this.parseTemporalExtent(extent);
        const indices = this.getFilteredTemporalIndices(dimension.name, parsedExtent.start, parsedExtent.end);

        this._filter(axis, indices);
        dimension.labels = indices.map(i => temporalLabels[i]);
    }

    aggregateTemporal(intervals, reducer, labels, dimensionName, context) {
        const dimension = dimensionName ? this.getDimensionByName(dimensionName) : this.getTemporalDimension();

        const axis = this.dimensions.findIndex((e) => e.name === dimension.name);
        const data = this.data;
        const newValues = [];
        const computedLabels = [];

        for (let interval of intervals) {
            computedLabels.push(interval[0]);
            const parsedInterval = this.parseTemporalExtent(interval);
            const indices = this.getFilteredTemporalIndices(dimension.name, parsedInterval.start, parsedInterval.end);

            const allCoords = this._iterateCoords(data.shape.slice(), [axis]);
            for (let coord of allCoords) {
                const entireDataToReduce = convert_to_1d_array(data.pick.apply(data, coord));
                const dataToReduce = indices.map((index) => entireDataToReduce[index]);

                const newVals = reducer({
                    data: dataToReduce,
                    context: context,
                });
                newValues.push(newVals);
            }
        }

        const newShape = data.shape.slice();
        newShape[axis] = intervals.length;
        this.data = ndarray(newValues, newShape);
        dimension.labels = labels && labels.length > 0 ? labels : computedLabels;
    }

    parseTemporalExtent(extent) {
        if (extent.length !== 2) {
            throw new Error("Invalid temporal extent. Temporal extent must be an array of exactly two elements.");
        }

        if (extent[0] === null && extent[1] === null) {
            throw new Error("Invalid temporal extent. Only one of the boundaries can be null.");
        }

        const start = parse_rfc3339(extent[0]);
        const end = parse_rfc3339(extent[1]);

        if ((extent[0] !== null && !start) || (extent[1] !== null && !end)) {
            throw new Error("Invalid temporal extent. Boundary must be ISO date string or null.");
        }

        return {
            start: extent[0] === null ? null : start,
            end: extent[1] === null ? null : end
        }
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