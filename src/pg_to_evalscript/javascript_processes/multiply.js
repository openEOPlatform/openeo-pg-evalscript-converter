function multiply(arguments) {
  const { x, y } = arguments;

  validateParameter({
    processName: "multiply",
    parameterName: "x",
    value: x,
    required: true,
    allowedTypes: ["number"],
  });

  validateParameter({
    processName: "multiply",
    parameterName: "y",
    value: y,
    required: true,
    allowedTypes: ["number"],
  });

  if (x === null || y === null) {
    return null;
  }

  return x * y;
}
