function rename_labels(arguments) {
    const {data, dimension, target, source} = arguments;
    for (let i = 0; i < target.length; i++) {
        const ind = data.bands.indexOf(source[i])
        data.bands[ind] = target[i]
    }
    return data;
}