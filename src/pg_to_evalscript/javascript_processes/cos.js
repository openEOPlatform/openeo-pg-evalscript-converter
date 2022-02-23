function cos(arguments) {
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

  // floating point handling in javascript is ... special
  // cos((n * PI) / 2) is not exactly 0 (for n = any int value)
  // TODO
  return Math.cos(x);
}