function arctan2(arguments) {
  const { x, y } = arguments;

  validateParameter({
    processName: "arctan2",
    parameterName: "x",
    value: x,
    required: true,
    allowedTypes: ["number"],
  });

  validateParameter({
    processName: "arctan2",
    parameterName: "y",
    value: y,
    required: true,
    allowedTypes: ["number"],
  });

  if (x === null || y === null) {
    return null;
  }

  return Math.atan2(y, x);
}
