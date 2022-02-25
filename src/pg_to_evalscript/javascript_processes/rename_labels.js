function rename_labels(arguments) {
  const { data, dimension, target, source = [] } = arguments;

  if (data === undefined) {
    throw new Error("Mandatory argument `data` is not defined.");
  }

  if (dimension === undefined) {
    throw new Error("Mandatory argument `dimension` is not defined.");
  }

  if (target === undefined) {
    throw new Error("Mandatory argument `target` is not defined.");
  }

  if (typeof dimension !== "string") {
    throw new Error("Argument `dimension` is not a string.");
  }

  if (!Array.isArray(target)) {
    throw new Error("Argument `target` is not an array.");
  }

  if (!Array.isArray(source)) {
    throw new Error("Argument `source` is not an array.");
  }

  if (
    !Array.isArray(data.getDimensionByName(dimension).labels) &&
    source.length === 0
  ) {
    throw new Error("The dimension labels are not enumerated.");
  }

  if (source.length === 0) {
    data.getDimensionByName(dimension).labels = target;
    return data;
  }

  if (target.length !== source.length) {
    throw new Error(
      "The number of labels in the parameters `source` and `target` do not match."
    );
  }

  for (let i = 0; i < target.length; i++) {
    if (typeof target[i] !== "number" && typeof target[i] !== "string") {
      throw new Error(
        "Element in argument `target` is not a number or a string."
      );
    }

    if (typeof source[i] !== "number" && typeof source[i] !== "string") {
      throw new Error(
        "Element in argument `source` is not a number or a string."
      );
    }

    if (data.getDimensionByName(dimension).labels.includes(target[i])) {
      throw new Error("A label with the specified name exists.");
    }

    const ind = data.getDimensionByName(dimension).labels.indexOf(source[i]);
    if (ind < 0) {
      throw new Error("A label with the specified name does not exist.");
    }

    data.getDimensionByName(dimension).labels[ind] = target[i];
  }
  return data;
}
