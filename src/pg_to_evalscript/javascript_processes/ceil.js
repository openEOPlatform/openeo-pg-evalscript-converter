function ceil(arguments) {
  const { x } = arguments;

  validateParameter({
    processName: "ceil",
    parameterName: "x",
    value: x,
    required: true,
    allowedTypes: ["number"],
  });

  if (x === null) {
    return null;
  }

  return Math.ceil(x);
}
