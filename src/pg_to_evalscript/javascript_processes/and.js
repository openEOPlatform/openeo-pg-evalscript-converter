function and(arguments) {
  const { x, y } = arguments;

  validateParameter({
    processName: "and",
    parameterName: "x",
    value: x,
    required: true,
    boolean: true,
  });

  validateParameter({
    processName: "and",
    parameterName: "y",
    value: y,
    required: true,
    boolean: true,
  });

  if (x === false || y === false) {
    return false;
  }

  if (x && y) {
    return true;
  }

  return null;
}
