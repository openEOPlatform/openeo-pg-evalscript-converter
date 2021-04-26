function add_dimension(arguments) {
    const {data, name, label, type} = arguments;
    console.log("At add dimension")
    console.dir(data)
    let newData = data.clone()
    newData.addDimension(name, label, type)
    console.dir(newData)
    console.log("~~~~~~~~~~~~~")
    return newData;
}