function array_contains(arguments) {
  const { data, value } = arguments;

  validateParameter({
    processName: "array_contains",
    parameterName: "data",
    value: data,
    required: true,
    nullable: false,
    array: true,
  });

  validateParameter({
    processName: "array_contains",
    parameterName: "value",
    value: value,
    required: true,
  });

  if (typeof value === "object" || value === null) {
    return false;
  }
  return data.includes(value);
}
