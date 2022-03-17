function sum(arguments) {
  const { data, ignore_nodata = true } = arguments;

  validateParameter({
    processName: "sum",
    parameterName: "data",
    value: data,
    required: true,
    nullable: false,
    array: true,
  });

  validateParameter({
    processName: "sum",
    parameterName: "ignore_nodata",
    value: ignore_nodata,
    nullable: false,
    allowedTypes: ["boolean"],
  });

  let sum = null;

  for (let x of data) {
    validateParameter({
      processName: "sum",
      parameterName: "element of data",
      value: x,
      allowedTypes: ["number"],
    });

    if (x === null) {
      if (ignore_nodata) {
        continue;
      } else {
        return null;
      }
    }

    if (sum === null) {
      sum = x;
    } else {
      sum += x;
    }
  }

  return sum;
}
