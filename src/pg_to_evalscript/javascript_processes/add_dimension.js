function add_dimension(arguments) {
  const { data, name, label, type = "other" } = arguments;

  if (data.getDimensionByName(name)) {
    throw new Error("A dimension with the specified name already exists.");
  }

  let newData = data.clone();
  newData.addDimension(name, label, type);
  return newData;
}
