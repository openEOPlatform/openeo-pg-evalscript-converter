function int(arguments) {
  const { x } = arguments;

  if (typeof x === undefined) {
    throw new Error("Mandatory argument `x` is not defined.");
  }

  if (x === null) {
    return null;
  }

  if (typeof x !== "number") {
    throw new Error("Argument `x` is not a number.");
  }

  return Math.trunc(x);
}
