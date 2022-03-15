function exp(arguments) {
  const { p } = arguments;

  validateParameter({
    processName: "exp",
    parameterName: "p",
    value: p,
    required: true,
    allowedTypes: ["number"],
  });

  if (p === null) {
    return null;
  }

  return Math.exp(p);
}
