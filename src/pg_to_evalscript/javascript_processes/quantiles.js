function quantiles(arguments) {
  const { data, probabilities, q, ignore_nodata = true } = arguments;

  validateParameter({
    processName: "quantiles",
    parameterName: "data",
    value: data,
    required: true,
    nullable: false,
    array: true,
  });

  validateParameter({
    processName: "quantiles",
    parameterName: "ignore_nodata",
    value: ignore_nodata,
    nullable: false,
    allowedTypes: ["boolean"],
  });

  if (probabilities === undefined && q === undefined) {
    throw new ProcessError({
      name: "QuantilesParameterMissing",
      message:
        "The process `quantiles` requires either the `probabilities` or `q` parameter to be set.",
    });
  }

  if (probabilities !== undefined && q !== undefined) {
    throw new ProcessError({
      name: "QuantilesParameterConflict",
      message:
        "The process `quantiles` only allows that either the `probabilities` or the `q` parameter is set.",
    });
  }

  let probs = [];

  if (q !== undefined) {
    validateParameter({
      processName: "quantiles",
      parameterName: "q",
      value: q,
      integer: true,
      min: 2,
    });

    const interval = 1 / q;
    for (let i = interval; i < 1; i += interval) {
      probs.push(i);
    }
  }

  if (probabilities !== undefined) {
    validateParameter({
      processName: "quantiles",
      parameterName: "probabilities",
      value: probabilities,
      array: true,
    });

    probs = probabilities;
  }

  let newData = [...data].sort((a, b) => a - b);

  if (!ignore_nodata && newData.includes(null)) {
    return Array.from(probs).fill(null);
  }

  newData = newData.filter((el) => el !== null);

  if (newData.length === 0) {
    return Array.from(probs).fill(null);
  }

  let quantiles = [];

  for (const el of probs) {
    if (!!probabilities && q === undefined) {
      validateParameter({
        processName: "quantiles",
        parameterName: "element of probabilities",
        value: el,
        allowedTypes: ["number"],
        min: 0,
        max: 1,
      });
    }

    const pos = (newData.length - 1) * el;
    const base = Math.floor(pos);
    const rest = pos - base;
    if (newData[base + 1] !== undefined) {
      quantiles.push(
        newData[base] + rest * (newData[base + 1] - newData[base])
      );
    } else {
      quantiles.push(newData[base]);
    }
  }

  return quantiles;
}
