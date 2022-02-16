function power(arguments) {
  const { p, base } = arguments;

  if (p === undefined || base === undefined) {
    throw new Error("Mandatory argument `p` or `base` is not defined.");
  }

  if (p === null || base === null) {
    return null;
  }

  if (typeof p !== "number") {
    throw new Error("Argument `p` is not a number.");
  }

  if (typeof base !== "number") {
    throw new Error("Argument `base` is not a number.");
  }

  return Math.pow(base, p);
}
