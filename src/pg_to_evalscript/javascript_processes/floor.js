function floor(arguments) {
  const { x } = arguments;

  validateParameter({
    processName: "floor",
    parameterName: "x",
    value: x,
    required: true,
    allowedTypes: ["number"],
  });

  if (x === null) {
    return null;
  }

  return Math.floor(x);
}
