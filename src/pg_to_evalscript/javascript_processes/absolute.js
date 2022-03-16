function absolute(arguments) {
  const { x } = arguments;

  validateParameter({
    processName: "absolute",
    parameterName: "x",
    value: x,
    required: true,
    allowedTypes: ["number"],
  });

  if (x === null) {
    return null;
  }

  return Math.abs(x);
}
