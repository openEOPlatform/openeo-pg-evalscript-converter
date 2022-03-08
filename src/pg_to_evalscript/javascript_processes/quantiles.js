function quantiles(arguments) {
  const { data, probabilities, q, ignore_nodata = true } = arguments;

  if (data === undefined || data === null) {
    throw new Error("Mandatory argument `data` is either null or not defined");
  }

  if (!Array.isArray(data)) {
    throw new Error("Argument `data` is not an array.");
  }

  if (typeof ignore_nodata !== "boolean") {
    throw new Error("Argument `ignore_nodata` is not a boolean.");
  }

  if (probabilities === undefined && q === undefined) {
    throw new ProcessError({
      name: "QuantilesParameterMissing",
      message: "The process `quantiles` requires either the `probabilities` or `q` parameter to be set."
    });
  }

  if (probabilities !== undefined && q !== undefined) {
    throw new ProcessError({
      name: "QuantilesParameterConflict",
      message: "The process `quantiles` only allows that either the `probabilities` or the `q` parameter is set."
    });
  }

  let probs = [];

  if (q !== undefined) {
    if (!Number.isInteger(q)) {
      throw new Error("Argument `q` is not an integer.");
    }

    if (q < 2) {
      throw new Error("Argument `q` must be greater or equal to 2.");
    }

    const interval = 1 / q;
    for (let i = interval; i < 1; i += interval) {
      probs.push(i);
    }
  }

  if (probabilities !== undefined) {
    if (!Array.isArray(probabilities)) {
      throw new Error("Argument `probabilities` is not an array.");
    }

    probs = probabilities;
  }

  let newData = [...data].sort((a, b) => a - b);

  if (!ignore_nodata && newData.includes(null)) {
    return Array.from(probs).fill(null);
  }

  newData = newData.filter(el => el !== null);

  if (newData.length === 0) {
    return Array.from(probs).fill(null);
  }

  let quantiles = [];

  for (const el of probs) {
    if (!!probabilities && q === undefined) {
      if (typeof el !== 'number') {
        throw new Error("Element in argument `probabilities` is not a number.");
      }
      if (el < 0 || el > 1) {
        throw new Error("Elements in argument `probabilities` must be between 0 and 1 (both inclusive).");
      }
    }

    const pos = (newData.length - 1) * el;
    const base = Math.floor(pos);
    const rest = pos - base;
    if (newData[base + 1] !== undefined) {
      quantiles.push(newData[base] + rest * (newData[base + 1] - newData[base]));
    } else {
      quantiles.push(newData[base]);
    }
  }

  return quantiles;
}