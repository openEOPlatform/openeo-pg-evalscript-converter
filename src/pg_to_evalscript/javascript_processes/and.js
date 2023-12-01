function and(arguments) {
  const startTime = Date.now();
  const { x, y } = arguments;

  validateParameter({
    processName: "and",
    parameterName: "x",
    value: x,
    required: true,
    allowedTypes: ["boolean"],
  });

  validateParameter({
    processName: "and",
    parameterName: "y",
    value: y,
    required: true,
    allowedTypes: ["boolean"],
  });

  if (x === false || y === false) {
    const endTime = Date.now();
    executionTimes.push({ fun: "and.js", params: {}, success: true, time: endTime - startTime });
    return false;
  }

  if (x && y) {
    const endTime = Date.now();
    executionTimes.push({ fun: "and.js", params: {}, success: true, time: endTime - startTime });
    return true;
  }

  const endTime = Date.now();
  executionTimes.push({ fun: "and.js", params: {}, success: true, time: endTime - startTime });
  return null;
}
