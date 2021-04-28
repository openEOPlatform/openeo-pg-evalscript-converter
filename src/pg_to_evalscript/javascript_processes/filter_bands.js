function filter_bands(arguments) {
    const {data, bands} = arguments;
    const newData = data.clone()
    console.log("At filter bands")
    console.dir(newData.clone())
    newData.filterBands(bands);
    console.dir(newData.clone())
    console.log("#######################")
    return newData;
}