function any(arguments) {
  const { data, ignore_nodata = true } = arguments;

  validateParameter({
    processName: "any",
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
        boolean: true,
      });

      if (x === null) {
        continue;
      }

      if (x === true) {
        returnVal = true;
        break;
      }

      returnVal = false;
    }

    return returnVal;
  }

  if (data.length === 1) {
    return data[0];
  }

  return data.reduce((x, y) => {
    validateParameter({
      processName: "all",
      parameterName: "element of data",
      value: x,
      boolean: true,
    });

    validateParameter({
      processName: "all",
      parameterName: "element of data",
      value: y,
      boolean: true,
    });

    if (x === true || y === true) {
      return true;
    }
    if (x === false && y === false) {
      return false;
    }
    return null;
  }, null);
}
