function lte(arguments) {
  const { x, y } = arguments;
  const supportedTypes = ["number", "string", "boolean"];

  validateParameter({
    processName: "lte",
    parameterName: "x",
    value: x,
    required: true,
  });

  validateParameter({
    processName: "lte",
    parameterName: "y",
    value: y,
    required: true,
  });

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
    return xAsISODateString.value <= yAsISODateString.value;
  }

  return x === y;
}
