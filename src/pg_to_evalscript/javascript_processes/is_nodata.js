function is_nodata(arguments) {
  const { x } = arguments;

  if (x === undefined) {
    throw Error("Process is_nodata requires argument x.");
  }

  return x === null;
}
