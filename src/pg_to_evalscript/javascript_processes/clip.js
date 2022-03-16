function clip(arguments) {
  const { x, min, max } = arguments;

  validateParameter({
    processName: "clip",
    parameterName: "x",
    value: x,
    required: true,
    allowedTypes: ["number"],
  });

  validateParameter({
    processName: "clip",
    parameterName: "min",
    value: min,
    required: true,
    allowedTypes: ["number"],
  });

  validateParameter({
    processName: "clip",
    parameterName: "max",
    value: max,
    required: true,
    allowedTypes: ["number"],
  });

  if (x === null) {
    return null;
  }

  if (x < min) {
    return min;
  }

  if (x > max) {
    return max;
  }

  return x;
}
