function any(arguments) {
  const { data, ignore_nodata = true } = arguments;

  if (data === undefined) {
    throw new Error("Mandatory argument `data` is not defined.");
  }

  if (!Array.isArray(data)) {
    throw new Error("Argument `data` is not an array.");
  }

  if (!data.every((x) => typeof x === "boolean" || x === null)) {
    throw new Error(
      "Values in argument `data` can only be of type boolean or null."
    );
  }

  if (ignore_nodata) {
    if (data.filter((x) => x !== null).length === 0) {
      return null;
    }
    return data.filter((x) => x !== null).some((x) => x === true);
  }

  if (data.length === 0) {
    return null;
  }

  return data.reduce((x, y) => {
    if (x === true || y === true) {
      return true;
    }
    if (x === false && y === false) {
      return false;
    }
    return null;
  });
}
