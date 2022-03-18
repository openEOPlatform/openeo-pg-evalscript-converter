function int(arguments) {
  const { x } = arguments;

  validateParameter({
    processName: "int",
    parameterName: "x",
    value: x,
    required: true,
    allowedTypes: ["number"],
  });

  if (x === null) {
    return null;
  }

  return Math.trunc(x);
}
