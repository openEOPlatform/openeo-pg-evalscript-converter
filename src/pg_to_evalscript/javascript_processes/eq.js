function eq(arguments) {
  const { x, y, delta = null, case_sensitive = true } = arguments;
  if (x === undefined) {
    throw Error("Process eq requires argument x.");
  }

  if (y === undefined) {
    throw Error("Process eq requires argument y.");
  }

  if (x === null || y === null) {
    return null;
  }

  if (typeof x !== typeof y) {
    return false;
  }

  if (
    (typeof x !== "number" && typeof x !== "string") ||
    (typeof y !== "number" && typeof y !== "string")
  ) {
    return false;
  }

  if (typeof x === "number" && delta) {
    return Math.abs(x - y) <= delta;
  }

  const xAsISODateString = parse_rfc3339(x);
  const yAsISODateString = parse_rfc3339(y);

  if (xAsISODateString && yAsISODateString) {
    return xAsISODateString === yAsISODateString;
  } else {
    return case_sensitive ? x === y : x.toLowerCase() === y.toLowerCase();
  }
}
