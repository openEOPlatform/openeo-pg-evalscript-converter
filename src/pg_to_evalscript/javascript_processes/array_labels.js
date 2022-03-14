function array_labels(arguments) {
  const { data } = arguments;

  if (data === undefined) {
    throw new Error("Mandatory argument `data` is not defined.");
  }

  if (!Array.isArray(data)) {
    throw new Error("Argument `data` is not an array.");
  }

  if (data.labels === undefined) {
    throw new Error("Argument `data` is not a labeled array.");
  }

  if (!Array.isArray(data.labels)) {
    throw new Error("Labels in argument `data` is not an array.");
  }

  return data.labels;
}
