function array_append(arguments) {
  const { data, value } = arguments;
  if (data === null || data === undefined) {
    throw new Error(
      "Mandatory argument `data` is either null or not defined."
    );
  }
  if (value === undefined) {
    throw new Error(
      "Mandatory argument `value` is not defined."
    );
  }
  if (!Array.isArray(data)) {
    throw new Error("Argument `data` is not an array.");
  }
  return [...data, value];
}
