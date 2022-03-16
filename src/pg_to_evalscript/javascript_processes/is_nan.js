function is_nan(arguments) {
  const { x } = arguments;

  validateParameter({
    processName: "is_nan",
    parameterName: "x",
    value: x,
    required: true,
  });

  if (x === null) {
    return true;
  }

  return isNaN(x);
}
