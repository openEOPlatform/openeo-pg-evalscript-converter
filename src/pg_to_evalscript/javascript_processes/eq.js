function eq(arguments) {
  const { x, y, delta = null, case_sensitive = true } = arguments;
  const supportedTypes = ["number", "string", "boolean"];

  validateParameter({
    processName: "eq",
    parameterName: "x",
    value: x,
    required: true,
  });

  validateParameter({
    processName: "eq",
    parameterName: "y",
    value: y,
    required: true,
  });

  if (x === null || y === null) {
    return null;
  }

  if (typeof x !== typeof y) {
    return false;
  }

  if (
    supportedTypes.indexOf(typeof x) === -1 ||
    supportedTypes.indexOf(typeof y) === -1
  ) {
    return false;
  }

  if (typeof x === "number" && delta) {
    return Math.abs(x - y) <= delta;
  }

  const xAsISODateString = parse_rfc3339(x);
  const yAsISODateString = parse_rfc3339(y);

  if (xAsISODateString && yAsISODateString) {
    return xAsISODateString.value === yAsISODateString.value;
  } else {
    return case_sensitive ? x === y : x.toLowerCase() === y.toLowerCase();
  }
}
