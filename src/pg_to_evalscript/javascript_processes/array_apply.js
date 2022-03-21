function array_apply(arguments) {
  const { data, process, context = null } = arguments;

  validateParameter({
    processName: "array_apply",
    parameterName: "data",
    value: data,
    required: true,
    nullable: false,
    array: true,
  });

  validateParameter({
    processName: "array_apply",
    parameterName: "process",
    value: process,
    required: true,
    nullable: false,
    allowedTypes: ["function"],
  });

  let newData = [];
  for (let i = 0; i < data.length; i++) {
    newData[i] = process({
      x: data[i],
      index: i,
      label: data.labels ? data.labels[i] : undefined,
      context: context,
    });
  }

  return newData;
}
