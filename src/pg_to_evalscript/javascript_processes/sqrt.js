function sqrt(arguments) {
  const { x } = arguments;

  validateParameter({
    processName: "sqrt",
    parameterName: "x",
    value: x,
    required: true,
    allowedTypes: ["number"],
    min: 0,
  });

  if (x === null) {
    return null;
  }

  return Math.sqrt(x);
}
