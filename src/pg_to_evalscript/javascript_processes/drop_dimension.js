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
    throw new ProcessError({
      name: "DimensionNotAvailable",
      message: "A dimension with the specified name does not exist.",
    });
  }

  const dimIndex = data.dimensions.findIndex((d) => d.name === name);
  const dimData = data.getDataShape();
  if (dimData[dimIndex] > 1) {
    throw new ProcessError({
      name: "DimensionLabelCountMismatch",
      message:
        "The number of dimension labels exceeds one, which requires a reducer.",
    });
  }

  let newData = data.clone();
  newData.removeDimension(name);
  return newData;
}
