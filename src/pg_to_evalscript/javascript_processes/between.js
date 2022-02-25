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

  const xAsISODateString = parse_rfc3339(x);
  const minAsISODateString = parse_rfc3339(min);
  const maxAsISODateString = parse_rfc3339(max);

  if (xAsISODateString && minAsISODateString && maxAsISODateString) {
    let maxValue = maxAsISODateString.value;
    let excludeMax = exclude_max;

    // handle special case where max is interval representing whole day
    // so one day is added and upper limit is excluded
    if (maxAsISODateString.type === "date" && !exclude_max) {
      const nextDay = new Date(maxAsISODateString.value);
      nextDay.setDate(nextDay.getDate() + 1);
      maxValue = nextDay.toISOString();
      excludeMax = true;
    }

    return isBetween(
      xAsISODateString.value,
      minAsISODateString.value,
      maxValue,
      excludeMax
    );
  } else {
    return isBetween(x, min, max, exclude_max);
  }
}
