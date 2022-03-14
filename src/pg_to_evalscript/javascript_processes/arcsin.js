function arcsin(arguments) {
  const { x } = arguments;

  validateParameter({
    processName: "arcsin",
    parameterName: "x",
    value: x,
    required: true,
    allowedTypes: ["number"],
  });

  if (x === null) {
    return null;
  }

  return Math.asin(x);
}
