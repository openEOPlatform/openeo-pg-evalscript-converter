function ndvi(arguments) {
  const { data, nir = "nir", red = "red", target_band = null } = arguments;

  validateParameter({
    processName: "ndvi",
    parameterName: "data",
    value: data,
    nullable: false,
    required: true,
  });

  validateParameter({
    processName: "ndvi",
    parameterName: "nir",
    value: nir,
    nullable: false,
    allowedTypes: ["string"],
  });

  validateParameter({
    processName: "ndvi",
    parameterName: "red",
    value: red,
    nullable: false,
    allowedTypes: ["string"],
  });

  validateParameter({
    processName: "ndvi",
    parameterName: "target_band",
    value: target_band,
    allowedTypes: ["string"],
  });

  let bandsDim = data.dimensions.find((d) => d.type === data.BANDS);
  if (!bandsDim) {
    throw new ProcessError({
      name: "DimensionAmbiguous",
      message: "Dimension of type `bands` is not available or is ambiguous.",
    });
  }

  if (!bandsDim.labels.includes(nir)) {
    throw new ProcessError({
      name: "NirBandAmbiguous",
      message:
        "The NIR band can't be resolved, please specify the specific NIR band name.",
    });
  }

  if (!bandsDim.labels.includes(red)) {
    throw new ProcessError({
      name: "RedBandAmbiguous",
      message:
        "The red band can't be resolved, please specify the specific red band name.",
    });
  }

  if (target_band !== null && bandsDim.labels.includes(target_band)) {
    throw new ProcessError({
      name: "BandExists",
      message: "A band with the specified target name exists.",
    });
  }

  const clonedData = data.clone();
  bandsDim = clonedData.dimensions.find((d) => d.type === clonedData.BANDS);
  const [nirIdx, redIdx] = clonedData.getBandIndices([nir, red]);
  if (target_band !== null) {
    const newShape = clonedData.getDataShape();
    const axis = clonedData.dimensions.findIndex(
      (d) => d.type === clonedData.BANDS
    );
    bandsDim.labels.push(target_band);
    const dataArr = clonedData.data.data;
    const len = newShape
      .filter((_, i) => i !== axis)
      .reduce((a, b) => a * b, 1);
    for (let step = 0; step < len; step++) {
      const n = dataArr[nirIdx + step * newShape[axis] + step];
      const r = dataArr[redIdx + step * newShape[axis] + step];
      const ndvi = (n - r) / (n + r);
      dataArr.splice(newShape[axis] + step * newShape[axis] + step, 0, ndvi);
    }
    newShape[axis]++;
    clonedData.data = ndarray(dataArr, newShape);
    return clonedData;
  }

  clonedData.reduceByDimension(
    ({ data }) => (data[nirIdx] - data[redIdx]) / (data[nirIdx] + data[redIdx]),
    bandsDim.name
  );
  return clonedData;
}
