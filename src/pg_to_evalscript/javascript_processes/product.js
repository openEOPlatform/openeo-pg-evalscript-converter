function product(arguments) {
  const { data, ignore_nodata = true } = arguments;

  validateParameter({
    processName: "product",
    parameterName: "data",
    value: data,
    required: true,
    array: true,
  });

  validateParameter({
    processName: "product",
    parameterName: "ignore_nodata",
    value: ignore_nodata,
    nullable: false,
    allowedTypes: ["boolean"],
  });

  let product = 1;
  for (let x of data) {
    validateParameter({
      processName: "product",
      parameterName: "element of data",
      value: x,
      allowedTypes: ["number"],
    });

    if (x === null) {
      if (ignore_nodata) {
        continue;
      } else {
        product = null;
        break;
      }
    }

    product = product * x;
  }

  if (data.length === 0) {
    product = null;
  }

  return product;
}
