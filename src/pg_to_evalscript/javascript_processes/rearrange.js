function rearrange(arguments) {
  const { data, order } = arguments;

  validateParameter({
    processName: "rearrange",
    parameterName: "data",
    value: data,
    required: true,
    nullable: false,
    array: true,
  });

  validateParameter({
    processName: "rearrange",
    parameterName: "order",
    value: order,
    required: true,
    nullable: false,
    array: true,
  });

  let newData = [];

  for (let el of order) {
    validateParameter({
      processName: "rearrange",
      parameterName: "element of order",
      value: el,
      integer: true,
      min: 0,
    });

    if (data[el] === undefined) {
      throw new Error(
        "Argument `order` contains an index which does not exist in argument `data`."
      );
    }

    newData.push(data[el]);
  }

  return newData;
}
