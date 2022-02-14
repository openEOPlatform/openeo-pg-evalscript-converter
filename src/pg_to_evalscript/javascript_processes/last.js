function last(arguments) {
  const { data, ignore_nodata = true } = arguments;

  if (data === null || data === undefined) {
    throw new Error("Mandatory argument `data` is either null or not defined.");
  }

  if (data.length === 0 || data.every((x) => x === null)) {
    return null;
  }

  if (ignore_nodata) {
    return [...data].reverse().find((x) => x !== null);
  }

  return [...data].pop();
}
