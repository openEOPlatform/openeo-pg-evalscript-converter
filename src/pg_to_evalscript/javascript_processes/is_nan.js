function is_nan(arguments) {
  const { x } = arguments;

  if (x === undefined) {
    throw Error("Process is_nan requires argument x.");
  }

  if (x === null) {
    return true;
  }

  return isNaN(x);
}
