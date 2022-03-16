function normalized_difference(arguments) {
  const { x, y } = arguments;

  validateParameter({
    processName: "normalized_difference",
    parameterName: "x",
    value: x,
    required: true,
    nullable: false,
    allowedTypes: ["number"],
  });

  validateParameter({
    processName: "normalized_difference",
    parameterName: "y",
    value: y,
    required: true,
    nullable: false,
    allowedTypes: ["number"],
  });

  if (x === -y) {
    throw new Error("Division by zero is not supported.");
  }

  return (x - y) / (x + y);
}
