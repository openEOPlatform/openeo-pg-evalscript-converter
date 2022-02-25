function normalized_difference(arguments) {
  const { x, y } = arguments;

  if (x === undefined) {
    throw new Error("Mandatory argument `x` is not defined.");
  }

  if (y === undefined) {
    throw new Error("Mandatory argument `y` is not defined.");
  }

  if (typeof x !== "number") {
    throw new Error("Argument `x` is not a number.");
  }

  if (typeof y !== "number") {
    throw new Error("Argument `y` is not a number.");
  }

  if (x === -y) {
    throw new Error("Division by zero is not supported.");
  }

  return (x - y) / (x + y);
}
