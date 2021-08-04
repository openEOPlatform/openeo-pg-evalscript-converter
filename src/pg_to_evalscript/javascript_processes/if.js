function _if(arguments) {
    const {value, accept, reject=null} = arguments;
    if(value === true) {
        return accept
    }
    return reject
}