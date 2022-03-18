function power(arguments) {
  const { p, base } = arguments;

  validateParameter({
    processName: "power",
    parameterName: "p",
    value: p,
    required: true,
    allowedTypes: ["number"],
  });

  validateParameter({
    processName: "power",
    parameterName: "base",
    value: base,
    required: true,
    allowedTypes: ["number"],
  });

  if (p === null || base === null) {
    return null;
  }

  return Math.pow(base, p);
}
