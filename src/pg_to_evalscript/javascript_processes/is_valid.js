function is_valid(arguments) {
  const { x } = arguments;

  if (x === undefined) {
    throw Error("Process is_valid requires argument x.");
  }

  if (x == null) {
    return false;
  }

  if (typeof x === "number") {
    return !isNaN(x) && isFinite(x);
  }

  return true;
}
