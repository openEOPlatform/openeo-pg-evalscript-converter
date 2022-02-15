function exp(arguments) {
  const { p } = arguments;

  if (p === undefined) {
    throw new Error("Mandatory argument `p` is not defined.");
  }

  if (p === null) {
    return null;
  }

  if (typeof p !== "number") {
    throw new Error("Argument `p` is not a number.");
  }

  return Math.exp(p);
}
