function log(arguments) {
  const { x, base } = arguments;

  if (x === undefined || base === undefined) {
    throw new Error("Mandatory argument `x` or `base` is not defined.");
  }

  if (x === null || base === null) {
    return null;
  }

  if (typeof x !== "number") {
    throw new Error("Argument `x` is not a number.");
  }

  if (typeof base !== "number") {
    throw new Error("Argument `base` is not a number.");
  }

  return Math.log(x) / Math.log(base);
}
