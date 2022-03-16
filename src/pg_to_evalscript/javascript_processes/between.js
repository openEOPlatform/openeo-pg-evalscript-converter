function between(arguments) {
  const isBetween = (x, min, max, exclude_max) => {
    let result = x >= min && x <= max;
    if (exclude_max) {
      result &= x < max;
    }
    return result;
  };

  const { x, min, max, exclude_max = false } = arguments;

  validateParameter({
    processName: "between",
    parameterName: "x",
    value: x,
    required: true,
  });

  if (x === null) {
    return null;
  }

  validateParameter({
    processName: "between",
    parameterName: "min",
    value: min,
    required: true,
    nullable: false,
  });

  validateParameter({
    processName: "between",
    parameterName: "max",
    value: max,
    required: true,
    nullable: false,
  });

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
