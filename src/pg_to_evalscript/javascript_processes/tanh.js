function tanh(arguments) {
  const { x } = arguments;

  validateParameter({
    processName: "tanh",
    parameterName: "x",
    value: x,
    required: true,
    allowedTypes: ["number"],
  });

  if (x === null) {
    return null;
  }

  return Math.tanh(x);
}
