function gt(arguments) {
  const { x, y } = arguments;

  if (x === undefined) {
    throw Error("Process gt requires argument x.");
  }

  if (y === undefined) {
    throw Error("Process gt requires argument y.");
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

  return x > y;
}
