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

  function getDataForDimension(data, currLevel, dimLevel) {
    if (currLevel === dimLevel) {
      return data;
    }
    return getDataForDimension(data[0], currLevel + 1, dimLevel);
  }

  const dimLevel = data.dimensions.findIndex((d) => d.name === name);
  const dimData = getDataForDimension(data.data, 0, dimLevel);
  if (dimData.length > 1) {
    throw new Error(
      "The number of dimension labels exceeds one, which requires a reducer."
    );
  }

  let newData = data.clone();
  newData.removeDimension(name);
  return newData;
}
