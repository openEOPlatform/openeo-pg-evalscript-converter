function mean(arguments) {
const startTime = Date.now();
  const { data, ignore_nodata = true } = arguments;

  validateParameter({
    processName: "mean",
    parameterName: "data",
    value: data,
    required: true,
    array: true,
  });

  validateParameter({
    processName: "mean",
    parameterName: "ignore_nodata",
    value: ignore_nodata,
    nullable: false,
    allowedTypes: ["boolean"],
  });

  let sum = 0;
  let el_num = 0;

  for (let x of data) {
    validateParameter({
      processName: "mean",
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

    sum += x;
    el_num++;
  }

  if (el_num === 0) {
    return null;
  }

const endTime = Date.now();
executionTimes.push({ fun: "mean.js", params: {}, success: true, time: endTime - startTime });
  return sum / el_num;
}
