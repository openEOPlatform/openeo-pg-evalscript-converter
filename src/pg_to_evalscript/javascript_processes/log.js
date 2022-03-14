function log(arguments) {
  const { x, base } = arguments;

  validateParameter({
    processName: "log",
    parameterName: "x",
    value: x,
    required: true,
    allowedTypes: ["number"],
  });

  validateParameter({
    processName: "log",
    parameterName: "base",
    value: base,
    required: true,
    allowedTypes: ["number"],
  });

  if (x === null || base === null) {
    return null;
  }

  return Math.log(x) / Math.log(base);
}
