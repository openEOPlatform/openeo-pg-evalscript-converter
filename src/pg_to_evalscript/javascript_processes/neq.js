function neq(arguments) {
  const { x, y, delta = null, case_sensitive = true } = arguments;
  const supportedTypes = ["number", "string", "boolean"];

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
    supportedTypes.indexOf(typeof x) === -1 ||
    supportedTypes.indexOf(typeof y) === -1
  ) {
    return false;
  }

  if (typeof x === "number" && delta) {
    return Math.abs(x - y) > delta;
  }

  const xAsISODateString = parse_rfc3339(x);
  const yAsISODateString = parse_rfc3339(y);

  if (xAsISODateString && yAsISODateString) {
    return xAsISODateString !== yAsISODateString;
  } else {
    return case_sensitive ? x !== y : x.toLowerCase() !== y.toLowerCase();
  }
}