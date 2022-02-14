function array_concat(arguments) {
  const { array1, array2 } = arguments;
  if (array1 === null || array1 === undefined) {
    throw new Error(
      "Mandatory argument `array1` is either null or not defined."
    );
  }
  if (array2 === null || array2 === undefined) {
    throw new Error(
      "Mandatory argument `array2` is either null or not defined."
    );
  }
  return [...array1, ...array2];
}
