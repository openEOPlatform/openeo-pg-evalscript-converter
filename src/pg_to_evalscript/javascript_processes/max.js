function max(arguments) {
const startTime = Date.now();
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

const endTime = Date.now();
executionTimes.push({ fun: "max.js", params: {}, success: true, time: endTime - startTime });
  return maxVal;
}


// x = [1, 2, 10, null, 39, 23, null, 4, 4, null, 6, 2, 1]
// x.sort((a, b) => b - a) // add value validation
// x[0] : MAX
// x[x.length - 1] : IF NULL -> no_data exists in data