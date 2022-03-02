function array_interpolate_linear(arguments) {
  const { data } = arguments;

  if (data === null || data === undefined) {
    throw new Error(
      "Mandatory argument `data` is either null or not defined."
    );
  }

  const linear_interpolation = (v0, v1, t) => (1 - t) * v0 + t * v1;
  let newData = [...data];
  let start = newData[0];
  let end = newData[0];
  let nullIndices = [];

  for (let i = 0; i < newData.length; i++) {
    if (newData[i] === null) {
      if (i === 0 || i === newData.length - 1) {
        continue;
      }

      nullIndices.push(i);
      continue;
    }

    if (typeof newData[i] !== "number") {
      throw new Error("Element in `data` is not of correct type.");
    }

    end = newData[i];

    if (start !== null && end !== null) {
      for (let j = 0; j < nullIndices.length; j++) {
        const t = (j + 1) / (nullIndices.length + 1);

        newData[nullIndices[j]] = linear_interpolation(start, end, t);
      }
    }

    start = newData[i];
    nullIndices = [];
  }

  return newData;
}