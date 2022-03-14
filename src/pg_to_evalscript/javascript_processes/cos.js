function cos(arguments) {
  const { x } = arguments;

  validateParameter({
    processName: "cos",
    parameterName: "x",
    value: x,
    required: true,
    allowedTypes: ["number"],
  });

  if (x === null) {
    return null;
  }

  return Math.cos(x);
}
