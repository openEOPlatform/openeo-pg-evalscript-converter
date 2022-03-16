function sinh(arguments) {
  const { x } = arguments;

  validateParameter({
    processName: "sinh",
    parameterName: "x",
    value: x,
    required: true,
    allowedTypes: ["number"],
  });

  if (x === null) {
    return null;
  }

  return Math.sinh(x);
}
