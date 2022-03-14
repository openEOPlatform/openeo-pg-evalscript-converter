function _if(arguments) {
  const { value, accept, reject = null } = arguments;

  validateParameter({
    processName: "if",
    parameterName: "value",
    value: value,
    required: true,
    allowedTypes: ["boolean"],
  });

  validateParameter({
    processName: "if",
    parameterName: "accept",
    value: accept,
    required: true,
  });

  if (value === true) {
    return accept;
  }

  return reject;
}
