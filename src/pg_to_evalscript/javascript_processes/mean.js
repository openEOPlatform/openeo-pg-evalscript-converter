function mean(arguments) {
    const {data} = arguments;
    return data.reduce((prev, curr) => prev + curr)/data.length
}