function filter_bands(arguments) {
    const {data, bands} = arguments;
    if (Array.isArray(data)) {
        return data.forEach(s => bands.map(b => s[b]))
    }
    return bands.map(b => data[b])
}