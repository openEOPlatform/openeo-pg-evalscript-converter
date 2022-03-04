function _if(arguments) {
  const { value, accept, reject = null } = arguments;

  if (value === undefined) {
    throw new Error("Mandatory argument `value` is not defined.");
  }

  if (accept === undefined) {
    throw new Error("Mandatory argument `accept` is not defined.");
  }

  if (typeof value !== "boolean" && value !== null) {
    throw new Error("Argument `value` is not a boolean or null.");
  }

  if (value === true) {
    return accept;
  }

  return reject;
}
