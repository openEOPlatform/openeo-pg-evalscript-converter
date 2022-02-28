function rearrange(arguments) {
  const { data, order} = arguments;

  if (data === null || data === undefined) {
    throw new Error("Mandatory argument `data` is either null or not defined.");
  }

  if (order === null || order === undefined) {
    throw new Error("Mandatory argument `order` is either null or not defined.");
  }

  if (!Array.isArray(data)) {
    throw new Error("Argument `data` is not an array.");
  }

  let newData = [];

  for (let el of order) {
    if (!Number.isInteger(el) || el < 0){
      throw new Error("Argument `order` must contain only integer values greater than or equal to 0.");
    }
    if(data[el] === undefined){
      throw new Error("Argument `order` contains an index which does not exist in argument `data`.");
    }

    newData.push(data[el]);
  }

  return newData;
}