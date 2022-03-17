function array_filter(arguments) {
  const { data, condition: cond, context } = arguments;

  validateParameter({
    processName: "array_filter",
    parameterName: "data",
    value: data,
    required: true,
    array: true,
  });

  validateParameter({
    processName: "array_filter",
    parameterName: "condition",
    value: cond,
    required: true,
  });

  let filteredData = [];

  for (let i = 0; i < data.length; i++) {
    if (condition({ x: data[i], index: i, label: data.labels ? data.labels[i] : undefined, context })) {
      filteredData.push(data[i]);
    }
  }

  return filteredData;
}
