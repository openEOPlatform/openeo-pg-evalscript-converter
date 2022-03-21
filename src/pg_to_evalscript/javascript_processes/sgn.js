function sgn(arguments) {
  const { x } = arguments;

  validateParameter({
    processName: "sgn",
    parameterName: "x",
    value: x,
    required: true,
    allowedTypes: ["number"],
  });

  if (x === null) {
    return null;
  }

  if (x > 0) {
    return 1;
  }

  if (x < 0) {
    return -1;
  }

  return 0;
}
