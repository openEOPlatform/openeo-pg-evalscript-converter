function arctan2(arguments) {
  const { x, y } = arguments;

  if (x === undefined && y === undefined) {
    throw new Error("Mandatory arguments `x` and `y` are not defined.");
  }

  if (x === undefined) {
    throw new Error("Mandatory argument `x` is not defined.");
  }

  if (y === undefined) {
    throw new Error("Mandatory argument `y` is not defined.");
  }

  if(x === null || y === null){
    return null;
  }

  if (typeof x !== "number") {
    throw new Error("Argument `x` is not a number.");
  }

  if (typeof y !== "number") {
    throw new Error("Argument `y` is not a number.");
  }

  return Math.atan2(y, x);
}