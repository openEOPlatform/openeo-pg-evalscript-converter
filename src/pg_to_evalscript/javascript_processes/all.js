function all(arguments) {
  const { data, ignore_nodata = true } = arguments;

  if (data === undefined) {
    throw new Error("Mandatory argument `data` is not defined.");
  }

  if (!Array.isArray(data)) {
    throw new Error("Argument `data` is not an array.");
  }

  if (ignore_nodata) {
    let returnVal = null;
    for (let x of data) {
      if (typeof x !== "boolean" && x !== null) {
        throw new Error(
          "Values in argument `data` can only be of type boolean or null."
        );
      }

      if (x === null) {
        continue;
      }

      if (x === false) {
        returnVal = false;
        break;
      }

      returnVal = true;
    }

    return returnVal;
  }

  if (data.length === 1) {
    return data[0];
  }

  return data.reduce((x, y) => {
    if (
      (typeof x !== "boolean" && x !== null) ||
      (typeof y !== "boolean" && y !== null)
    ) {
      throw new Error(
        "Values in argument `data` can only be of type boolean or null."
      );
    }

    if (x === false || y === false) {
      return false;
    }
    if (x === true && y === true) {
      return true;
    }
    return null;
  }, null);
}
