function add_dimension(arguments) {
  const { data, name, label, type = "other" } = arguments;

  if (data === undefined) {
    throw new Error("Mandatory argument `data` is not defined.");
  }

  if (name === undefined) {
    throw new Error("Mandatory argument `name` is not defined.");
  }

  if (label === undefined) {
    throw new Error("Mandatory argument `label` is not defined.");
  }

  if (typeof name !== "string") {
    throw new Error("Argument `name` is not a string.");
  }

  if (typeof label !== "number" && typeof label !== "string") {
    throw new Error("Argument `label` is not a string or a number.");
  }

  if (typeof type !== "string") {
    throw new Error("Argument `type` is not a string.");
  }

  if (data.getDimensionByName(name)) {
    throw new Error("A dimension with the specified name already exists.");
  }

  let newData = data.clone();
  newData.addDimension(name, label, type);
  return newData;
}
