function count(arguments) {
  const { data, condition = null, context = null } = arguments;

  if (data === undefined) {
    throw new Error("Mandatory argument `data` is not defined.");
  }

  if (!Array.isArray(data)) {
    throw new Error("Argument `data` is not an array.");
  }

  if (
    typeof condition !== "boolean" &&
    typeof condition === "object" &&
    Array.isArray(condition) &&
    condition !== null
  ) {
    throw new Error("Argument `condition` is not a boolean, object or null.");
  }

  if (condition && context) {
    condition.context = { ...context, ...condition.context };
  }

  let count = 0;
  for (let val of data) {
    if (condition === null && is_valid({ x: val })) {
      count++;
      continue;
    }

    if (condition === true) {
      count++;
      continue;
    }

    if (condition !== null && condition({ x: val })) {
      count++;
      continue;
    }
  }

  return count;
}
