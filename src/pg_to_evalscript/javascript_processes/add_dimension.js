function add_dimension(arguments) {
    const {data, name, label, type} = arguments;
    let newData = data.clone()
    newData.addDimension(name, label, type)
    return newData;
}