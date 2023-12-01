function all(arguments) {
  const startTime = Date.now();
  const { data, ignore_nodata = true } = arguments;

  validateParameter({
    processName: "all",
    parameterName: "data",
    value: data,
    required: true,
    array: true,
  });

  if (ignore_nodata) {
    let returnVal = null;
    for (let x of data) {
      validateParameter({
        processName: "all",
        parameterName: "element of data",
        value: x,
        allowedTypes: ["boolean"],
      });

      if (x === null) {
        continue;
      }

      if (x === false) {
        returnVal = false;
        break;
      }

      returnVal = true;
    }
    const endTime = Date.now();
    executionTimes.push({ fun: "all.js", params: {}, success: true, time: endTime - startTime });
    return returnVal;
  }

  if (data.length === 1) {
    const endTime = Date.now();
    executionTimes.push({ fun: "all.js", params: {}, success: true, time: endTime - startTime });
    return data[0];
  }

  return data.reduce((x, y) => {
    validateParameter({
      processName: "all",
      parameterName: "element of data",
      value: x,
      allowedTypes: ["boolean"],
    });

    validateParameter({
      processName: "all",
      parameterName: "element of data",
      value: y,
      allowedTypes: ["boolean"],
    });

    if (x === false || y === false) {
      const endTime = Date.now();
      executionTimes.push({ fun: "all.js", params: {}, success: true, time: endTime - startTime });
      return false;
    }
    if (x === true && y === true) {
      const endTime = Date.now();
      executionTimes.push({ fun: "all.js", params: {}, success: true, time: endTime - startTime });
      return true;
    }
    const endTime = Date.now();
    executionTimes.push({ fun: "all.js", params: {}, success: true, time: endTime - startTime });
    return null;
  }, null);
}
