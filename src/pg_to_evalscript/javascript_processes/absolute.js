function absolute(arguments) {
  const { x } = arguments;

  if (x === null) {
    return null;
  }

  if (x === undefined) {
    throw Error("Process absolute requires argument x.");
  }

  return Math.abs(x);
}
