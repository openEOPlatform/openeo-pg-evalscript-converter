class DataCube {
    constructor(data, bands_dimension_name, temporal_dimension_name, fromSamples) {
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
        if (Array.isArray(samples)) {
            if(samples.length === 0) {
                return ndarray([])
            }
            if (this.getDimensionByName(this.bands_dimension_name).labels.length === 0) {
                this.getDimensionByName(this.bands_dimension_name).labels = Object.keys(samples[0])
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
        let newData = ndarray(this.data.data.slice(), this.data.shape)
        const axis = this.dimensions.findIndex(e => e.name === dimension)
        const shape = newData.shape
        const newShape = shape.slice()
        newShape.splice(axis, 1)
        const coords = fill(shape.slice(), 0);
        coords[axis] = null;
        const labels = this.dimensions[axis].labels
        const newValues = []
        let currInd = 0;

        while (true) {
            if (coords.length > 1 && coords[currInd] === null) {
                currInd++
            }
            if (currInd >= shape.length) {
                break;
            }
            const dataToReduce = convert_to_1d_array(newData.pick.apply(newData, coords))
            dataToReduce.labels = labels
            const newVals = reducer({
                data: dataToReduce,
                context: context
            })
            newValues.push(newVals)
            if (coords.length === 1) {
                break;
            }
            if (coords[currInd] + 1 >= shape[currInd]) {
                currInd++
            } else {
                coords[currInd]++
            }
        }
        this.data = ndarray(newValues, newShape)
        this.dimensions.splice(axis, 1)
    }

    getDataShape() {
        return this.data.shape;
    }

    _addDimension(axis) {
        // new dimension is added before the axis
        this.data.shape.splice(axis, 0, 1)
        this.data = ndarray(this.data.data, this.data.shape)
    }

    _select(arr, coordArr) {
        // coordArr: 1D list of n coordinates. If m-th place has `null`, the entire axis is included and the dimension is kept
        function coordInSlice(c1, sliceArr) {
            return sliceArr.every((e, i) => e === null || e === c1[i])
        }
        return this._iter(arr, (a, coords) => {
            if (coordInSlice(coords, coordArr)) {
                return a
            }
        }, coords => coords.length >= coordArr.length || coordArr[coords.length] === null ? false : true)
    }

    _set(arr, vals, coordArr) {
        // Set values at coordArr
        function coordInSlice(c1, sliceArr) {
            return c1.length === sliceArr.length && sliceArr.every((e, i) => e === null || e === c1[i])
        }
        const exec_set = (a, coords) => {
            if (coordInSlice(coords, coordArr)) {
                let valueToSet;
                if (Array.isArray(vals)) {
                    valueToSet = this._select(vals, coordArr.map((c, i) => c === null ? coords[i] : null).filter(c => c !== null))
                } else {
                    valueToSet = vals
                }
                return valueToSet
            }
            return a
        }
        return this._iter(arr, exec_set)
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
}