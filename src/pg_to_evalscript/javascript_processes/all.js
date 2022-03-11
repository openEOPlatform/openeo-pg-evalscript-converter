function all(arguments) {
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
        boolean: true,
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

    if (x === false || y === false) {
      return false;
    }
    if (x === true && y === true) {
      return true;
    }
    return null;
  }, null);
}
