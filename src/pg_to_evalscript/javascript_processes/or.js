function or(arguments) {
  const { x, y } = arguments;

  validateParameter({
    processName: "or",
    parameterName: "x",
    value: x,
    required: true,
    allowedTypes: ["boolean"],
  });

  validateParameter({
    processName: "or",
    parameterName: "y",
    value: y,
    required: true,
    allowedTypes: ["boolean"],
  });

  if (x === true || y === true) {
    return true;
  }

  if (x === false && y === false) {
    return false;
  }

  return null;
}
