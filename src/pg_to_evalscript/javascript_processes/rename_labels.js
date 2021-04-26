function rename_labels(arguments) {
    const {data, dimension, target, source} = arguments;
    console.log("In rename labels")
    console.dir(data)
    for (let i = 0; i < target.length; i++) {
        const ind = data.getDimensionByName(dimension).labels.indexOf(source[i])
        data.getDimensionByName(dimension).labels[ind] = target[i]
    }
    console.dir(data)
    console.log("=================================")
    return data;
}