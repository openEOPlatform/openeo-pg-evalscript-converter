function divide(arguments) {
  const { x, y } = arguments;

  validateParameter({
    processName: "divide",
    parameterName: "x",
    value: x,
    required: true,
    allowedTypes: ["number"],
  });

  validateParameter({
    processName: "divide",
    parameterName: "y",
    value: y,
    required: true,
    allowedTypes: ["number"],
  });

  if (x === null || y === null) {
    return null;
  }

  if (y === 0) {
    throw new Error("Division by zero is not supported.");
  }

  return x / y;
}
