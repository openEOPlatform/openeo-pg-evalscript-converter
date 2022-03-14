function is_nodata(arguments) {
  const { x } = arguments;

  validateParameter({
    processName: "is_nodata",
    parameterName: "x",
    value: x,
    required: true,
  });

  return x === null;
}
