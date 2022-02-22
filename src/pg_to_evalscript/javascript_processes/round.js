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

  if (!Number.isInteger(p)) {
    throw new Error("Argument `p` is not an integer.");
  }

  if (p < 0) {
    return (
      Math.round(x / Math.pow(10, Math.abs(p))) * Math.pow(10, Math.abs(p))
    );
  }

  if (p === 0) {
    if (Math.abs(x) - Math.trunc(Math.abs(x)) === 0.5) {
      if (Math.floor(x) % 2 === 0) {
        return Math.floor(x);
      } else {
        return Math.ceil(x);
      }
    }
  }

  return Number(x.toFixed(p));
}
