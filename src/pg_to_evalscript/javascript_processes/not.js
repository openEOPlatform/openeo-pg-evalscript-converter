function not(arguments) {
  const { x } = arguments;

  if (x === undefined) {
    throw new Error("Mandatory argument `x` is not defined.");
  }

  if (x === null) {
    return null;
  }

  if (typeof x !== "boolean") {
    throw new Error("Argument `x` is not a boolean.");
  }

  return !x;
}
