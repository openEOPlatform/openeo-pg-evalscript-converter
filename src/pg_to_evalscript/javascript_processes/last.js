function last(arguments) {
  const { data, ignore_nodata = true } = arguments;

  validateParameter({
    processName: "last",
    parameterName: "data",
    value: data,
    required: true,
    nullable: false,
  });

  if (data.length === 0 || data.every((x) => x === null)) {
    return null;
  }

  if (ignore_nodata) {
    return [...data].reverse().find((x) => x !== null);
  }

  return [...data].pop();
}
