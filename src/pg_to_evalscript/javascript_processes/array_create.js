function array_create(arguments) {
  const { data = [], repeat = 1 } = arguments;

  if (!Array.isArray(data)) {
    throw new Error("Argument `data` is not an array.");
  }

  if (!Number.isInteger(repeat)) {
    throw new Error("Argument `repeat` is not an integer.");
  }

  if (repeat < 1) {
    throw new Error(
      "Argument `repeat` must contain only values greater than or equal to 1."
    );
  }

  let newData = [];

  for (let i = 0; i < repeat; i++) {
    newData = [...newData, ...data];
  }

  return newData;
}
