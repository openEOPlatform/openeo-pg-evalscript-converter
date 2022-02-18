function round(arguments) {
  const { x, p = 0 } = arguments;

  if (typeof x === undefined) {
    throw new Error("Mandatory argument `x` is not defined.");
  }

  if (x === null) {
    return null;
  }

  if (typeof x !== "number") {
    throw new Error("Argument `x` is not a number.");
  }

  if (typeof p !== "number") {
    throw new Error("Argument `p` is not a number.");
  }

  if (p < 0) {
    return (
      Math.round(x / Math.pow(10, Math.abs(p))) * Math.pow(10, Math.abs(p))
    );
  }
  return Number(x.toFixed(p));
}
