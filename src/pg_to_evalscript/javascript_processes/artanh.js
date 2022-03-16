function artanh(arguments) {
  const { x } = arguments;

  validateParameter({
    processName: "artanh",
    parameterName: "x",
    value: x,
    required: true,
    allowedTypes: ["number"],
  });

  if (x === null) {
    return null;
  }

  return Math.atanh(x);
}
