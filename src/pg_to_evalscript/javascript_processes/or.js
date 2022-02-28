function or(arguments) {
  const { x, y } = arguments;

  if (x === undefined) {
    throw new Error("Mandatory argument `x` is not defined.");
  }

  if (y === undefined) {
    throw new Error("Mandatory argument `y` is not defined.");
  }

  if (typeof x !== "boolean" && x !== null) {
    throw new Error("Argument `x` is not a boolean or null.");
  }

  if (typeof y !== "boolean" && y !== null) {
    throw new Error("Argument `y` is not a boolean or null.");
  }

  if (x === true || y === true) {
    return true;
  }

  if (x === false && y === false) {
    return false;
  }

  return null;
}
