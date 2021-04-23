function array_element(arguments) {
    const {data, index, label} = arguments;
    if (index !== undefined) {
        return data[index]
    }
    data[data.labels.indexOf(label)]
}