function ln(arguments) {
  const { x } = arguments;

  validateParameter({
    processName: "ln",
    parameterName: "x",
    value: x,
    required: true,
    allowedTypes: ["number"],
  });

  if (x === null) {
    return null;
  }

  return Math.log(x);
}
