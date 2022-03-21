function apply(arguments) {
  const { data, process } = arguments;

  validateParameter({
    processName: "apply",
    parameterName: "data",
    value: data,
    nullable: false,
    required: true,
  });

  validateParameter({
    processName: "apply",
    parameterName: "process",
    value: process,
    nullable: false,
    required: true,
  });

  const newData = data.clone();
  newData.apply(process);
  return newData;
}
