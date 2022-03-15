function dimension_labels(arguments) {
  const { data, dimension } = arguments;

  if (data === undefined) {
    throw new Error("Mandatory argument `data` is not defined.");
  }

  if (dimension === undefined) {
    throw new Error("Mandatory argument `dimension` is not defined.");
  }

  if (typeof dimension !== "string") {
    throw new Error("Argument `dimension` is not a string.");
  }

  const dim = data.getDimensionByName(dimension);
  if (!dim) {
    throw new Error("A dimension with the specified name does not exist.");
  }

  if (!dim.labels) {
    throw new Error("Dimension is missing attribute labels.");
  }

  if (!Array.isArray(dim.labels)) {
    throw new Error("Dimension labels is not an array.");
  }

  return dim.labels;
}
