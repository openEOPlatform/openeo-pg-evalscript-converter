function add_dimension(arguments) {
    const {data, name, label, type} = arguments;
    data.addDimension(data, name, type)
    return data;
}