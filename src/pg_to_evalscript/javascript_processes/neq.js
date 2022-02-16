function neq(arguments) {
  const { x, y, delta = null, case_sensitive = true } = arguments;
  if (x === undefined) {
    throw Error("Process neq requires argument x.");
  }

  if (y === undefined) {
    throw Error("Process neq requires argument y.");
  }

  if (x === null || y === null) {
    return null;
  }

  if (typeof x !== typeof y) {
    return true;
  }

  if (
    (typeof x !== "number" && typeof x !== "string") ||
    (typeof y !== "number" && typeof y !== "string")
  ) {
    return false;
  }

  if (typeof x === "number" && delta) {
    return Math.abs(x - y) > delta;
  }

  if (typeof x === "string" && !case_sensitive) {
    return x.toLowerCase() !== y.toLowerCase();
  }

  return x !== y;
}
