function between(arguments) {
  const { x, min, max, exclude_max = false } = arguments;

  if (x === null) {
    return null;
  }

  if (x === undefined) {
    throw Error("Process between requires argument x.");
  }

  if (min === null || min === undefined) {
    throw Error("Process between requires argument min.");
  }

  if (max === null || max === undefined) {
    throw Error("Process between requires argument max.");
  }

  if (min > max) {
    return false;
  }

  let result = x >= min && x <= max;

  if (exclude_max) {
    result &= x < max;
  }

  return result;
}
