function subtract(arguments) {
  const { x, y } = arguments;

  validateParameter({
    processName: "subtract",
    parameterName: "x",
    value: x,
    required: true,
    allowedTypes: ["number"],
  });

  validateParameter({
    processName: "subtract",
    parameterName: "y",
    value: y,
    required: true,
    allowedTypes: ["number"],
  });

  if (x === null || y === null) {
    return null;
  }

  return x - y;
}
