function mod(arguments) {
  const { x, y } = arguments;

  if (x === undefined) {
    throw new Error("Mandatory argument `x` is not defined.");
  }

  if (y === undefined) {
    throw new Error("Mandatory argument `y` is not defined.");
  }

  if (y === 0) {
    throw new Error("Division by zero is not supported.");
  }

  if (x === null || y === null) {
    return null;
  }

  if (typeof x !== "number") {
    throw new Error("Argument `x` is not a number.");
  }

  if (typeof y !== "number") {
    throw new Error("Argument `y` is not a number.");
  }

  return Math.sign(y) * (Math.abs(x) % Math.abs(y));
}
