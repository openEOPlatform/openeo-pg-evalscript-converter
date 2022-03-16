function sin(arguments) {
  const { x } = arguments;

  validateParameter({
    processName: "sin",
    parameterName: "x",
    value: x,
    required: true,
    allowedTypes: ["number"],
  });

  if (x === null) {
    return null;
  }

  return Math.sin(x);
}
