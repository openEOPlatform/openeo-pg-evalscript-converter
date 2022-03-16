function arccos(arguments) {
  const { x } = arguments;

  validateParameter({
    processName: "arccos",
    parameterName: "x",
    value: x,
    required: true,
    allowedTypes: ["number"],
  });

  if (x === null) {
    return null;
  }

  return Math.acos(x);
}
