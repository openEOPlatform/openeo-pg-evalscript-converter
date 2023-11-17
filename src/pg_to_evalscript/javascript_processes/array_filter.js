function array_filter(arguments) {
  const startTime = Date.now();
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

  const endTime = Date.now();
  executionTimes.push({ fun: "array_filter.js", params: {}, success: true, time: endTime - startTime });
  return filteredData;
}
