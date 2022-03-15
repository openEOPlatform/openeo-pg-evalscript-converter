function array_create(arguments) {
  const { data = [], repeat = 1 } = arguments;

  validateParameter({
    processName: "array_create",
    parameterName: "data",
    value: data,
    array: true,
  });

  validateParameter({
    processName: "array_create",
    parameterName: "repeat",
    value: repeat,
    integer: true,
    min: 1,
  });

  let newData = [];

  for (let i = 0; i < repeat; i++) {
    newData = [...newData, ...data];
  }

  return newData;
}
