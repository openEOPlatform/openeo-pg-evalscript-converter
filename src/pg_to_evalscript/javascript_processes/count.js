function count(arguments) {
  const { data, condition: cond = null } = arguments;

  validateParameter({
    processName: "count",
    parameterName: "data",
    value: data,
    required: true,
    array: true,
  });

  validateParameter({
    processName: "count",
    parameterName: "condition",
    required: true,
    value: cond,
    allowedTypes: ["boolean", "object"],
  });

  if (cond !== null && Array.isArray(cond)) {
    throw new ValidationError({
      name: VALIDATION_ERRORS.WRONG_TYPE,
      message: `Value for condition is not boolean or object.`,
    });
  }

  if (cond === true) {
    return data.length;
  }

  let count = 0;
  for (let val of data) {
    if (cond === null && is_valid({ x: val })) {
      count++;
      continue;
    }

    if (cond !== null && condition({ x: val })) {
      count++;
      continue;
    }
  }

  return count;
}
