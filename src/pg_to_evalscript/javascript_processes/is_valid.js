function is_valid(arguments) {
  const { x } = arguments;

  validateParameter({
    processName: "is_valid",
    parameterName: "x",
    value: x,
    required: true,
  });

  if (x == null) {
    return false;
  }

  if (typeof x === "number") {
    return !isNaN(x) && isFinite(x);
  }

  return true;
}
