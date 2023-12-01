function extrema(arguments) {
  const startTime = Date.now();
  const { data, ignore_nodata = true } = arguments;

  validateParameter({
    processName: "extrema",
    parameterName: "data",
    value: data,
    required: true,
    array: true,
  });

  validateParameter({
    processName: "extrema",
    parameterName: "ignore_nodata",
    value: ignore_nodata,
    nullable: false,
    allowedTypes: ["boolean"],
  });

  let minVal = null;
  let maxVal = null;

  for (let x of data) {
    validateParameter({
      processName: "extrema",
      parameterName: "element of data",
      value: x,
      allowedTypes: ["number"],
    });

    if (x === null) {
      if (ignore_nodata) {
        continue;
      } else {
        minVal = null;
        maxVal = null;
        break;
      }
    }

    if (minVal === null) {
      minVal = x;
    }

    if (maxVal === null) {
      maxVal = x;
    }

    if (x < minVal) {
      minVal = x;
    }

    if (x > maxVal) {
      maxVal = x;
    }
  }

  const endTime = Date.now();
  executionTimes.push({ fun: "extrema.js", params: {}, success: true, time: endTime - startTime });
  return [minVal, maxVal];
}
