function lte(arguments) {
  const { x, y } = arguments;
  const supportedTypes = ["number", "string", "boolean"];

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
    supportedTypes.indexOf(typeof x) === -1 ||
    supportedTypes.indexOf(typeof y) === -1
  ) {
    return false;
  }

  if (typeof x !== typeof y) {
    return false;
  }

  if (typeof x === "number") {
    return x <= y;
  }

  if (typeof x === "boolean") {
    return x === y;
  }

  const xAsISODateString = parse_rfc3339(x);
  const yAsISODateString = parse_rfc3339(y);

  if (xAsISODateString && yAsISODateString) {
    return xAsISODateString <= yAsISODateString;
  }

  return x === y;
}
