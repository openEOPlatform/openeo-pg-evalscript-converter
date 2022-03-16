function cosh(arguments) {
  const { x } = arguments;

  validateParameter({
    processName: "cosh",
    parameterName: "x",
    value: x,
    required: true,
    allowedTypes: ["number"],
  });

  if (x === null) {
    return null;
  }

  return Math.cosh(x);
}
