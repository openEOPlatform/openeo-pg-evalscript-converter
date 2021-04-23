class DataCube {
  TEMPORAL = "TEMPORAL"
  BANDS = "BANDS"
  DIMENSIONS = [this.TEMPORAL, this.BANDS]

  constructor(data, bands_dimension_name, temporal_dimension_name) {
    this.data = this.makeArrayFromSamples(data)
    this.bands_dimension_name = bands_dimension_name;
    this.temporal_dimension_name = temporal_dimension_name;
  }

  makeArrayFromSamples(samples) {
    if (Array.isArray(samples)) {
      let newData = []
      for (let entry of samples) {
        if (!this.bands) {
          this.bands = Object.keys(entry)
        }
        newData.push(Object.values(entry))
      }
      return newData
    }
    else {
      if (!this.bands) {
        this.bands = Object.keys(samples)
      }
      return Object.values(samples)
    }
  }

  selectColumn(index) {
    return this.data.map(v => v[index])
  }

  getBandIndices(bands) {
    return bands.map(b => this.bands.indexOf(b))
  }

  filterBands(bands) {
    const indices = this.getBandIndices(bands)
    for(let i=0; i < this.data.length; i++) {
      this.data[i] = indices.map(ind => this.data[i][ind])
    }
    this.bands = bands;
  }

  removeDimension(dimension) {
    this.DIMENSIONS = this.DIMENSIONS.filter(d => d !== dimension)
  }

  reduceByDimension(reducer, dimension) {
    const newData = []
    if (dimension === this.temporal_dimension_name) {
      for (let i = 0; i < this.bands.length; i++) {
        const newValue = reducer({data: selectColumn(i)})
        newData.push(newValue)
      }
      this.removeDimension(this.TEMPORAL)
    }
    else if (dimension === this.bands_dimension_names) {
      for (let i = 0; i < this.data.length; i++) {
        let row = this.data[i]
        row.labels = [...this.bands]
        const newValue = reducer({data: row})
        this.data[i] = newValue;
      }
      this.removeDimension(this.BANDS)
    }
  }

  addDimension(data, name, type) {
  }

  clone() {
    const copy = new DataCube(JSON.parse(JSON.stringify(this.data)), this.bands_dimension_name, this.temporal_dimension_name)
    copy.bands = [...this.bands]
    copy.DIMENSIONS = [...this.DIMENSIONS]
    return copy
  }
}

[{B01: 3, B02: 6}, {B01: 2, B02: 1}, {B01: 4, B02: 5}]