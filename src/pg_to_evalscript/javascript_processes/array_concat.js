function array_concat(arguments) {
  const { array1, array2 } = arguments;

  validateParameter({
    processName: "array_concat",
    parameterName: "array1",
    value: array1,
    required: true,
    nullable: false,
    array: true,
  });

  validateParameter({
    processName: "array_concat",
    parameterName: "array2",
    value: array2,
    required: true,
    nullable: false,
    array: true,
  });

  return [...array1, ...array2];
}
