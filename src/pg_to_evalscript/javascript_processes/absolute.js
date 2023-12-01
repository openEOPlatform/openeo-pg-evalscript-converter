function absolute(arguments) {
  const startTime = Date.now();
  const { x } = arguments;

  validateParameter({
    processName: "absolute",
    parameterName: "x",
    value: x,
    required: true,
    allowedTypes: ["number"],
  });

  if (x === null) {
    return null;
  }

  const endTime = Date.now();
  executionTimes.push({ fun: "absolute.js", params: { x }, success: true, time: endTime - startTime });
  return Math.abs(x);
}
