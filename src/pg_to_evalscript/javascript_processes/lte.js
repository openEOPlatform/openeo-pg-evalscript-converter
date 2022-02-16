function lte(arguments) {
  const { x, y } = arguments;
  if (x === undefined) {
    throw Error("Process lte requires argument x.");
  }

  if (y === undefined) {
    throw Error("Process lte requires argument y.");
  }

  if (x === null || y === null) {
    return null;
  }

  if (
    (typeof x !== "number" && typeof x !== "string") ||
    (typeof y !== "number" && typeof y !== "string")
  ) {
    return false;
  }
  return x <= y;
}
