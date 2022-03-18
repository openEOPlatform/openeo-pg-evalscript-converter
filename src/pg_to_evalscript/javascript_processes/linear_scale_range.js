function linear_scale_range(arguments) {
  const { x, inputMin, inputMax, outputMin = 0, outputMax = 1 } = arguments;

  validateParameter({
    processName: "linear_scale_range",
    parameterName: "x",
    value: x,
    required: true,
    allowedTypes: ["number"],
  });

  if (x === null) {
    return null;
  }

  validateParameter({
    processName: "linear_scale_range",
    parameterName: "inputMin",
    value: inputMin,
    required: true,
    nullable: false,
    allowedTypes: ["number"],
  });

  validateParameter({
    processName: "linear_scale_range",
    parameterName: "inputMax",
    value: inputMax,
    required: true,
    nullable: false,
    allowedTypes: ["number"],
  });

  validateParameter({
    processName: "linear_scale_range",
    parameterName: "outputMin",
    value: outputMin,
    allowedTypes: ["number"],
  });

  validateParameter({
    processName: "linear_scale_range",
    parameterName: "outputMax",
    value: outputMax,
    allowedTypes: ["number"],
  });

  //The given number in x is clipped to the bounds specified in inputMin and inputMax
  const clippedValue = Math.min(inputMax, Math.max(x, inputMin));

  return (
    ((clippedValue - inputMin) / (inputMax - inputMin)) *
      (outputMax - outputMin) +
    outputMin
  );
}
