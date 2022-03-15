function arsinh(arguments) {
  const { x } = arguments;

  validateParameter({
    processName: "arsinh",
    parameterName: "x",
    value: x,
    required: true,
    allowedTypes: ["number"],
  });

  if (x === null) {
    return null;
  }

  return Math.asinh(x);
}
