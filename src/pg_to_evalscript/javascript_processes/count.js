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
    if (condition === true) {
      count++;
    }

    if (condition !== null && condition({ x: val })) {
      count++;
    }

    if (condition === null) {
      // still need to check every element if it is valid
      count++;
    }
  }

  return count;
}
