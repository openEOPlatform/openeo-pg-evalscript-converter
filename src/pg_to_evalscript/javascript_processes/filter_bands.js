function filter_bands(arguments) {
    const {data, bands} = arguments;
    const newData = data.clone()
    newData.filterBands(bands);
    return newData;
}