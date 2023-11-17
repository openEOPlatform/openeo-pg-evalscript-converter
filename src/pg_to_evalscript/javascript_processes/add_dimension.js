function add_dimension(arguments) {
  const startTime = Date.now();
  const { data, name, label, type = "other" } = arguments;

  validateParameter({
    processName: "add_dimension",
    parameterName: "data",
    value: data,
    required: true,
  });

  validateParameter({
    processName: "add_dimension",
    parameterName: "name",
    value: name,
    required: true,
    allowedTypes: ["string"],
  });

  validateParameter({
    processName: "add_dimension",
    parameterName: "label",
    value: label,
    required: true,
    allowedTypes: ["string", "number"],
  });

  validateParameter({
    processName: "add_dimension",
    parameterName: "type",
    value: type,
    allowedTypes: ["string"],
  });

  if (data.getDimensionByName(name)) {
    throw new Error("A dimension with the specified name already exists.");
  }

  let newData = data.clone();
  newData.addDimension(name, label, type);
  const endTime = Date.now();
  executionTimes.push({ fun: "add_dimension.js", params: {name, label, type}, success: true, time: endTime - startTime });
  return newData;
}
