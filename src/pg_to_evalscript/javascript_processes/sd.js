function sd(arguments) {
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

  let sum = 0;
  let count = 0;
  for (let x of data) {
    if (typeof x !== "number" && x !== null) {
      throw new Error("Value in argument `data` is not a number or null.");
    }

    if (x === null) {
      if (!ignore_nodata) {
        return null;
      } else {
        continue;
      }
    }

    sum += x;
    count++;
  }

  if (count === 0) {
    return null;
  }

  const mean = sum / count;
  let sumOfSquares = 0;
  for (let x of data) {
    if (ignore_nodata && x === null) {
      continue;
    }

    sumOfSquares += Math.pow(x - mean, 2);
  }

  return Math.sqrt(sumOfSquares / (count - 1));
}
