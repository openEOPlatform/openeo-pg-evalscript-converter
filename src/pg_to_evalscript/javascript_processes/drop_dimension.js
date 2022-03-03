function drop_dimension(arguments) {
  const { data, name } = arguments;

  if (data === undefined || data === null) {
    throw new Error("Mandatory argument `data` is either null or not defined.");
  }

  if (name === undefined || name === null) {
    throw new Error("Mandatory argument `name` is either null or not defined.");
  }

  if (typeof name !== "string") {
    throw new Error("Argument `name` is not a string.");
  }

  const dim = data.getDimensionByName(name);
  if (!dim) {
    throw new Error("A dimension with the specified name does not exist.");
  }

  if (dim.labels.length > 1) {
    throw new Error(
      "The number of dimension labels exceeds one, which requires a reducer."
    );
  }

  let newData = data.clone();
  newData.removeDimension(name);
  return newData;
}
