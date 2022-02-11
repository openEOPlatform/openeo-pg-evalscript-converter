function rename_labels(arguments) {
  const { data, dimension, target, source = [] } = arguments;

  if (!Array.isArray(data.getDimensionByName(dimension).labels) && !target) {
    throw new Error("The dimension labels are not enumerated.");
  }

  if (target.length !== source.length) {
    throw new Error(
      "The number of labels in the parameters `source` and `target` do not match."
    );
  }

  for (let i = 0; i < target.length; i++) {
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
