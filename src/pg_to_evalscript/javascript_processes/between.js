function between(arguments) {
  const isBetween = (x, min, max, exclude_max) => {
    let result = x >= min && x <= max;
    if (exclude_max) {
      result &= x < max;
    }
    return result;
  };

  const { x, min, max, exclude_max = false } = arguments;

  if (x === null) {
    return null;
  }

  if (x === undefined) {
    throw Error("Process between requires argument x.");
  }

  if (min === null || min === undefined) {
    throw Error("Process between requires argument min.");
  }

  if (max === null || max === undefined) {
    throw Error("Process between requires argument max.");
  }

  if (min > max) {
    return false;
  }

  let result = false;

  const xAsISODateString = parse_rfc3339(x);
  const minAsISODateString = parse_rfc3339(min);
  const maxAsISODateString = parse_rfc3339(max);

  if (xAsISODateString && minAsISODateString && maxAsISODateString) {
    result = isBetween(
      xAsISODateString,
      minAsISODateString,
      maxAsISODateString,
      exclude_max
    );
  } else {
    result = isBetween(x, min, max, exclude_max);
  }
  return result;
}
