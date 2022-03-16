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
    allowedTypes: ["object"],
  });

  return data.filter((val) => {
    return condition({ x: val });
  });
}
