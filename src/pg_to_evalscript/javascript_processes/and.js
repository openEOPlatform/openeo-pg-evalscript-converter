function and(arguments) {
  const { x, y } = arguments;

  validateParameter({
    processName: "and",
    parameterName: "x",
    value: x,
    required: true,
    allowedTypes: ["boolean"],
  });

  validateParameter({
    processName: "and",
    parameterName: "y",
    value: y,
    required: true,
    allowedTypes: ["boolean"],
  });

  if (x === false || y === false) {
    return false;
  }

  if (x && y) {
    return true;
  }

  return null;
}
