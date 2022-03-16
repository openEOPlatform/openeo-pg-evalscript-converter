function max(arguments) {
  const { data, ignore_nodata = true } = arguments;

  validateParameter({
    processName: "max",
    parameterName: "data",
    value: data,
    required: true,
    array: true,
  });

  validateParameter({
    processName: "max",
    parameterName: "ignore_nodata",
    value: ignore_nodata,
    nullable: false,
    allowedTypes: ["boolean"],
  });

  let maxVal = null;

  for (let x of data) {
    validateParameter({
      processName: "max",
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

    if (maxVal === null) {
      maxVal = x;
      continue;
    }

    if (x > maxVal) {
      maxVal = x;
    }
  }

  return maxVal;
}
