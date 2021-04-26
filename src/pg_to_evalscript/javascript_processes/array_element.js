function array_element(arguments) {
    const {data, index, label} = arguments;
    console.log("data at array_element")
    console.dir(data)
    if (index !== undefined) {
        return data[index]
    }
    console.log(data[data.labels.indexOf(label)])
    return data[data.labels.indexOf(label)]
}