function median(arguments) {
  const { data, ignore_nodata = true } = arguments;

  validateParameter({
    processName: "median",
    parameterName: "data",
    value: data,
    required: true,
    array: true,
  });

  validateParameter({
    processName: "median",
    parameterName: "ignore_nodata",
    value: ignore_nodata,
    nullable: false,
    allowedTypes: ["boolean"],
  });

  const newData = [];
  for (let i = 0; i < data.length; i++) {
    validateParameter({
      processName: "median",
      parameterName: "element of data",
      value: data[i],
      allowedTypes: ["number"],
    });

    if (data[i] === null) {
      if (ignore_nodata) {
        continue;
      } else {
        return null;
      }
    }

    newData.push(data[i]);
  }

  if (newData.length === 0) {
    return null;
  }

  newData.sort((a, b) => a - b);

  const bottomHalfIdx = Math.floor(newData.length / 2);
  if (bottomHalfIdx % 2 === 0) {
    return (newData[bottomHalfIdx - 1] + newData[bottomHalfIdx]) / 2;
  }

  return newData[bottomHalfIdx];
}
