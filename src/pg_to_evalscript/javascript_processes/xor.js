function xor(arguments) {
  const { x, y } = arguments;

  validateParameter({
    processName: "xor",
    parameterName: "x",
    value: x,
    required: true,
    allowedTypes: ["boolean"],
  });

  validateParameter({
    processName: "xor",
    parameterName: "y",
    value: y,
    required: true,
    allowedTypes: ["boolean"],
  });

  if (x === null || y === null) {
    return null;
  }

  return x === !y;
}
