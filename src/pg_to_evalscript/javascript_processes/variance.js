function variance(arguments) {
  const { data, ignore_nodata = true } = arguments;

  validateParameter({
    processName: "variance",
    parameterName: "data",
    value: data,
    required: true,
    nullable: false,
    array: true,
  });

  validateParameter({
    processName: "variance",
    parameterName: "ignore_nodata",
    value: ignore_nodata,
    nullable: false,
    allowedTypes: ["boolean"],
  });

  let sum = 0;
  let count = 0;
  for (let x of data) {
    validateParameter({
      processName: "variance",
      parameterName: "element of data",
      value: x,
      allowedTypes: ["number"],
    });

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

  if (count === 1) {
    return 0;
  }

  const mean = sum / count;
  let sumOfSquares = 0;
  for (let x of data) {
    if (ignore_nodata && x === null) {
      continue;
    }

    sumOfSquares += Math.pow(x - mean, 2);
  }

  return sumOfSquares / (count - 1);
}
