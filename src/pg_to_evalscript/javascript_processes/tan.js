function tan(arguments) {
  const { x } = arguments;

  validateParameter({
    processName: "tan",
    parameterName: "x",
    value: x,
    required: true,
    allowedTypes: ["number"],
  });

  if (x === null) {
    return null;
  }

  return Math.tan(x);
}
