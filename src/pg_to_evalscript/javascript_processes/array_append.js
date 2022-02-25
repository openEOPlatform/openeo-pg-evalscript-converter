function array_append(arguments) {
  const { array, value } = arguments;
  if (array === null || array === undefined) {
    throw new Error(
      "Mandatory argument `array` is either null or not defined."
    );
  }
  if (value === undefined) {
    throw new Error(
      "Mandatory argument `value` is not defined."
    );
  }
  if (!Array.isArray(array)) {
    throw new Error("Argument `array` is not an array.");
  }
  return [...array, value];
}
