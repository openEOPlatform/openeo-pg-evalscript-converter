function array_find(arguments) {
  const { data, value } = arguments;

  validateParameter({
    processName: "array_find",
    parameterName: "data",
    value: data,
    required: true,
    nullable: false,
    array: true,
  });

  validateParameter({
    processName: "array_find",
    parameterName: "value",
    value: value,
    required: true,
  });

  if (typeof value === "object" || value === null) {
    return null;
  }

  const index = data.indexOf(value);
  return (index === -1 ? null : index);
}
