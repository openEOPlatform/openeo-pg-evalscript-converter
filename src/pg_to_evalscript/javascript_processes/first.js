function first(arguments) {
  const { data, ignore_nodata = true } = arguments;

  validateParameter({
    processName: "first",
    parameterName: "data",
    value: data,
    required: true,
    nullable: false,
  });

  if (data.length === 0 || data.every((x) => x === null)) {
    return null;
  }

  if (ignore_nodata) {
    return data.find((x) => x !== null);
  }

  return data[0];
}
