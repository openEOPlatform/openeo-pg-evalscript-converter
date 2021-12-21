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
            let newData = []
            for (let entry of samples) {
                if (this.getDimensionByName(this.bands_dimension_name).labels.length === 0) {
                    this.getDimensionByName(this.bands_dimension_name).labels = Object.keys(entry)
                }
                newData.push(Object.values(entry))
            }
            return newData
        } else {
            if (this.getDimensionByName(this.bands_dimension_name).labels.length === 0) {
                this.getDimensionByName(this.bands_dimension_name).labels = Object.keys(samples)
            }
            return Object.values(samples)
        }
    }

    getBandIndices(bands) {
        return bands.map(b => this.getDimensionByName(this.bands_dimension_name).labels.indexOf(b))
    }

    filterBands(bands) {
        const indices = this.getBandIndices(bands)
        const axis = this.dimensions.findIndex(e => e.name === this.bands_dimension_name)
        this.data = this._filter(this.data, axis, indices)
        this.getDimensionByName(this.bands_dimension_name).labels = bands;
    }

    removeDimension(dimension) {
        this.dimensions = this.dimensions.filter(d => d.name !== dimension)
    }

    addDimension(name, label, type) {
        this.data = this._addDimension(this.data, 0)
        this.dimensions.unshift({
            name: name,
            labels: [label],
            type: type
        })
    }

    clone() {
        const copy = new DataCube(this._iter(this.data), this.bands_dimension_name, this.temporal_dimension_name)
        copy.dimensions = JSON.parse(JSON.stringify(this.dimensions))
        return copy
    }

    flattenToArray() {
        const flattenedData = this.flatten();
        return Array.isArray(flattenedData) ? flattenedData : [flattenedData]
    }

    encodeData() {
        const shape = this.getDataShape();
        const flattenedData = this.flattenToArray();
        return [...shape, ...flattenedData];
    }


    _iter(arr, execute = v => v, removeDim = () => false, execute_on_result = r => r, coords = []) {
        if (Array.isArray(arr)) {
            let result = []
            for (let i = 0; i < arr.length; i++) {
                const val = this._iter(arr[i], execute, removeDim, execute_on_result, [...coords, i])
                if (val !== undefined) {
                    result.push(val)
                }
            }
            result = execute_on_result(result, coords)
            if (result.length === 0) {
                return
            }
            const shouldRemoveDim = removeDim(coords)
            if (shouldRemoveDim && result.length !== 1) {
                throw new Error('Can only remove dimension of length 1!')
            } else if (shouldRemoveDim) {
                return result[0]
            }
            return result
        } else {
            return execute(arr, coords)
        }
    }

    reduceByDimension(reducer, dimension) {
        let newData = this._iter(this.data)
        const axis = this.dimensions.findIndex(e => e.name === dimension)
        const shape = this.getDataShape()
        const coords = new Array(shape.length).fill(0);
        coords[axis] = null;
        let currInd = 0;
        const labels = this.dimensions[axis].labels

        while (true) {
            if (currInd >= shape.length) {
                break;
            }
            const dataToReduce = this._select(newData, coords)
            dataToReduce.labels = labels
            const newVals = reducer({
                data: dataToReduce
            })
            newData = this._set(newData, newVals, coords)
            if (coords[currInd] + 1 >= shape[currInd]) {
                currInd++
            }
            if (coords[currInd] === null) {
                currInd++
            }
            coords[currInd]++
        }
        const finalSelectCoords = new Array(shape.length).fill(null);
        finalSelectCoords[axis] = 0;
        this.data = this._select(newData, finalSelectCoords);
        this.removeDimension(dimension)
    }

    flatten() {
        const flattenArr = (arr) => arr.reduce((flat, next) => flat.concat(next), []);
        return this._iter(this.data, v => v, () => false, r => {
            return flattenArr(r)
        })
    }

    getDataShape() {
        let dimensions;
        this._iter(this.data, (a, coords) => {
            dimensions = coords;
            return a
        })
        return dimensions.map(d => d + 1)
    }

    _addDimension(arr, axis) {
        // new dimension is added before the axis
        if (!Array.isArray(arr)) {
            return [arr]
        }
        return this._iter(arr, v => v, () => false, (r, c) => {
            if (c.length === axis) {
                return [r]
            }
            return r
        })
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

    _filter(arr, dim, coordArr) {
        const exec_filter = (a, coords) => {
            if (coordArr.includes(coords[dim])) {
                return a
            }
        }
        return this._iter(arr, exec_filter)
    }
}