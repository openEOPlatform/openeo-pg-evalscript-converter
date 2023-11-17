function add(arguments) {
  const startTime = Date.now();
  const { x, y } = arguments;

  validateParameter({
    processName: "add",
    parameterName: "x",
    value: x,
    required: true,
    allowedTypes: ["number"],
  });

  validateParameter({
    processName: "add",
    parameterName: "y",
    value: y,
    required: true,
    allowedTypes: ["number"],
  });

  if (x === null || y === null) {
    return null;
  }

  const endTime = Date.now();
  executionTimes.push({ fun: "add.js", params: {x,y}, success: true, time: endTime - startTime });
  return x + y;
}
