function gt(arguments) {
  const { x, y } = arguments;
  const supportedTypes = ["number", "string"];

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
    supportedTypes.indexOf(typeof x) === -1 ||
    supportedTypes.indexOf(typeof y) === -1
  ) {
    return false;
  }

  if (typeof x === "number" && typeof y === "number") {
    return x > y;
  }

  const xAsISODateString = parse_rfc3339(x);
  const yAsISODateString = parse_rfc3339(y);

  if (xAsISODateString && yAsISODateString) {
    return xAsISODateString > yAsISODateString;
  }

  return false;
}
