function clip(arguments) {
  const { x, min, max } = arguments;

  if (x === undefined) {
    throw new Error("Mandatory argument `x` is not defined.");
  }

  if (min === undefined) {
    throw new Error("Mandatory argument `min` is not defined.");
  }

  if (max === undefined) {
    throw new Error("Mandatory argument `max` is not defined.");
  }

  if (x === null) {
    return null;
  }

  if (typeof x !== "number") {
    throw new Error("Argument `x` is not a number.");
  }

  if (typeof min !== "number") {
    throw new Error("Argument `min` is not a number.");
  }

  if (typeof max !== "number") {
    throw new Error("Argument `max` is not a number.");
  }

  if (x < min) {
    return min;
  }

  if (x > max) {
    return max;
  }

  return x;
}
