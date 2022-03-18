function arcosh(arguments) {
  const { x } = arguments;

  validateParameter({
    processName: "arcosh",
    parameterName: "x",
    value: x,
    required: true,
    allowedTypes: ["number"],
  });

  if (x === null) {
    return null;
  }

  return Math.acosh(x);
}
