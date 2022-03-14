function array_append(arguments) {
  const { data, value } = arguments;

  validateParameter({
    processName: "array_append",
    parameterName: "data",
    value: data,
    required: true,
    nullable: false,
    array: true,
  });

  validateParameter({
    processName: "array_append",
    parameterName: "value",
    value: value,
    required: true,
  });

  return [...data, value];
}
