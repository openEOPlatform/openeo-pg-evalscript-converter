function rename_labels(arguments) {
    const {data, dimension, target, source} = arguments;
    for (let i = 0; i < target.length; i++) {
        const ind = data.getDimensionByName(dimension).labels.indexOf(source[i])
        data.getDimensionByName(dimension).labels[ind] = target[i]
    }
    return data;
}