function sgn(arguments) {
  const { x } = arguments;

  if (x === undefined) {
    throw new Error("Mandatory argument `x` is not defined.");
  }

  if (x === null) {
    return null;
  }

  if (typeof x !== "number") {
    throw new Error("Argument `x` is not a number.");
  }

  if (x > 0) {
    return 1;
  }

  if (x < 0) {
    return -1;
  }

  return 0;
}
