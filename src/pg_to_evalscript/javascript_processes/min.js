function min(arguments) {
const startTime = Date.now();
  const { data, ignore_nodata = true } = arguments;

  validateParameter({
    processName: "min",
    parameterName: "data",
    value: data,
    required: true,
    array: true,
  });

  validateParameter({
    processName: "min",
    parameterName: "ignore_nodata",
    value: ignore_nodata,
    nullable: false,
    allowedTypes: ["boolean"],
  });

  let minVal = null;

  for (let x of data) {
    validateParameter({
      processName: "min",
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

    if (minVal === null) {
      minVal = x;
      continue;
    }

    if (x < minVal) {
      minVal = x;
    }
  }

const endTime = Date.now();
executionTimes.push({ fun: "min.js", params: {}, success: true, time: endTime - startTime });
  return minVal;
}

// similar to max.js