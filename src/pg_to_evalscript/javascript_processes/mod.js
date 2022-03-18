function mod(arguments) {
  const { x, y } = arguments;

  validateParameter({
    processName: "mod",
    parameterName: "x",
    value: x,
    required: true,
    allowedTypes: ["number"],
  });

  validateParameter({
    processName: "mod",
    parameterName: "y",
    value: y,
    required: true,
    allowedTypes: ["number"],
  });

  if (y === 0) {
    throw new Error("Division by zero is not supported.");
  }

  if (x === null || y === null) {
    return null;
  }

  return Math.sign(y) * (Math.abs(x) % Math.abs(y));
}
