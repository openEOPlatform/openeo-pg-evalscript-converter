function drop_dimension(arguments) {
  const { data, name } = arguments;

  validateParameter({
    processName: "drop_dimension",
    parameterName: "data",
    value: data,
    nullable: false,
    required: true,
  });

  validateParameter({
    processName: "drop_dimension",
    parameterName: "name",
    value: name,
    nullable: false,
    required: true,
    allowedTypes: ["string"],
  });

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
