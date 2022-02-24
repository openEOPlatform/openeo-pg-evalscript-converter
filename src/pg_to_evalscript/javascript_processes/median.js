function median(arguments) {
  const { data, ignore_nodata = true } = arguments;

  if (data === undefined) {
    throw new Error("Mandatory argument `data` is not defined.");
  }

  if (!Array.isArray(data)) {
    throw new Error("Argument `data` is not an array.");
  }

  if (typeof ignore_nodata !== "boolean") {
    throw new Error("Argument `ignore_nodata` is not a boolean.");
  }

  const newData = [];
  for (let i = 0; i < data.length; i++) {
    if (typeof data[i] !== "number" && data[i] !== null) {
      throw new Error("Value in argument `data` is not a number or null.");
    }

    if (data[i] === null) {
      if (ignore_nodata) {
        continue;
      } else {
        return null;
      }
    }

    newData.push(data[i]);
  }

  if (newData.length === 0) {
    return null;
  }

  const bottomHalfIdx = Math.floor(newData.length / 2);
  if (bottomHalfIdx % 2 === 0) {
    return (newData[bottomHalfIdx - 1] + newData[bottomHalfIdx]) / 2;
  }

  return newData[bottomHalfIdx];
}
