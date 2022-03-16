function arctan(arguments) {
  const { x } = arguments;

  validateParameter({
    processName: "arctan",
    parameterName: "x",
    value: x,
    required: true,
    allowedTypes: ["number"],
  });

  if (x === null) {
    return null;
  }

  return Math.atan(x);
}
