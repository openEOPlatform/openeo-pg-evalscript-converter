function not(arguments) {
  const { x } = arguments;

  validateParameter({
    processName: "not",
    parameterName: "x",
    value: x,
    required: true,
    allowedTypes: ["boolean"],
  });

  if (x === null) {
    return null;
  }

  return !x;
}
