function count(arguments) {
  const { data, condition: cond = null } = arguments;

  if (data === undefined) {
    throw new Error("Mandatory argument `data` is not defined.");
  }

  if (!Array.isArray(data)) {
    throw new Error("Argument `data` is not an array.");
  }

  if (
    typeof cond !== "boolean" &&
    typeof cond === "object" &&
    Array.isArray(cond) &&
    cond !== null
  ) {
    throw new Error("Argument `condition` is not a boolean, object or null.");
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
