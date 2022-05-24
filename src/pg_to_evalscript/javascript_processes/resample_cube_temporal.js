function resample_cube_temporal(arguments) {
  const { data, target, dimension = null, valid_within = null } = arguments;

  validateParameter({
    processName: "resample_cube_temporal",
    parameterName: "data",
    value: data,
    required: true,
  });

  validateParameter({
    processName: "resample_cube_temporal",
    parameterName: "target",
    value: target,
    required: true,
  });

  validateParameter({
    processName: "resample_cube_temporal",
    parameterName: "dimension",
    value: dimension,
    required: false,
    allowedTypes: ["string"],
  });

  validateParameter({
    processName: "resample_cube_temporal",
    parameterName: "valid_within",
    value: valid_within,
    required: false,
    allowedTypes: ["number"],
  });


  let dataClone = data.clone();

  // find matching dimensions
  let temporalDimensionsPairs = [];
  if (dimension) {
    const dataDim = dataClone.getDimensionByName(dimension);
    const dataDimIndex = dataClone.dimensions.findIndex(d => d.name === targetDim.name);

    const targetDim = target.getDimensionByName(dimension);
    const targetDimIndex = target.dimensions.findIndex(d => d.name === targetDim.name);

    // provided dimension not present in one or both datacubes
    if (!dataDim || !targetDim) {
      throw new Error("DimensionNotAvailable");
    }

    if (dataDim.type !== dataClone.TEMPORAL || targetDim !== target.TEMPORAL) {
      throw new Error("DimensionMismatch");
    }

    temporalDimensionsPairs.push({ dataDim, dataDimIndex, targetDim, targetDimIndex });
  }
  else {
    for (let targetDimIndex in target.dimensions) {
      targetDimIndex = parseInt(targetDimIndex);
      const targetDim = target.dimensions[targetDimIndex];

      if (targetDim.type === target.TEMPORAL) {
        const dataDimIndex = dataClone.dimensions.findIndex(d => d.name === targetDim.name);
        const dataDim = dataClone.dimensions[dataDimIndex];

        if (dataDimIndex !== -1 && dataDim.type === dataClone.TEMPORAL) {
          temporalDimensionsPairs.push({ dataDim, dataDimIndex, targetDim, targetDimIndex });
        }
      }
    }

    if (temporalDimensionsPairs.length === 0) {
      throw new Error("DimensionMismatch");
    }
  }

  // go through pairs of matching temporal dimensions
  let resampledData = data.clone();
  for (let pair of temporalDimensionsPairs) {
    let { dataDim, dataDimIndex, targetDimIndex, targetDim } = pair;

    const targetDimSize = target.data.shape[targetDimIndex];

    // remove labels so the new ones can be easily added
    resampledData.dimensions[dataDimIndex].labels = [];

    // go through the TARGET labels (dates)
    for (let targetLabelIndex in targetDim.labels) {
      targetLabelIndex = parseInt(targetLabelIndex)

      let parsedTargetLabel = new Date(parse_rfc3339(targetDim.labels[targetLabelIndex]).value);
      let minDiff = Number.POSITIVE_INFINITY;
      let minDifParsedDataLabel = null;
      let nearestDataLabelIndex = 0;

      // find the nearest SOURCE label (date) for the current TARGET label (date)
      for (let dataLabelIndex in dataDim.labels) {
        dataLabelIndex = parseInt(dataLabelIndex);

        let parsedDataLabel = new Date(parse_rfc3339(dataDim.labels[dataLabelIndex]).value);
        let diff = Math.abs(parsedDataLabel - parsedTargetLabel);

        if (diff < minDiff) {
          minDiff = diff;
          minDifParsedDataLabel = parsedDataLabel;
          nearestDataLabelIndex = dataLabelIndex;
        }

        // DOCS: The rare case of ties is resolved by choosing the earlier timestamps.
        if (diff === minDiff) {
          if (parsedDataLabel < minDifParsedDataLabel) {
            minDiff = diff;
            minDifParsedDataLabel = parsedDataLabel;
            nearestDataLabelIndex = dataLabelIndex;
          }
        }
      }

      // pick the correct values (sub-ndarray) from SOURCE's ndarray
      const shapeArrayWithNullExceptLabelIndex = dataClone.dimensions.map(
        (d, i) => i == dataDimIndex ? nearestDataLabelIndex: null
      );
      const pickedNdarray = dataClone.data.pick(...shapeArrayWithNullExceptLabelIndex);
      const flatPickedNdarray = flattenToNativeArray(pickedNdarray, true);

      // transpose so that the temporal dimension is the outer-most, so it's easier to add the data
      const numOfDims = resampledData.data.shape.length;
      let swappedDims = [...Array(numOfDims).keys()];
      swappedDims[0] = dataDimIndex;
      swappedDims[dataDimIndex] = 0;
      resampledData.data = resampledData.data.transpose(...swappedDims);

      // update the shape and add the data
      resampledData.data.shape[0] = targetDimSize;
      resampledData.setInDimension(0, flatPickedNdarray, targetLabelIndex);
      resampledData.data = ndarray(flattenToNativeArray(resampledData.data, true), resampledData.data.shape);

      // transpose back to the original order of the axes
      resampledData.data = resampledData.data.transpose(...swappedDims);

      // add the label
      resampledData.dimensions[dataDimIndex].labels[targetLabelIndex] = dataDim.labels[nearestDataLabelIndex];
    }

    // create a new ndarray with correct shape so that the stride is correct too
    resampledData.data = ndarray(flattenToNativeArray(resampledData.data, true), resampledData.data.shape);
  }

  return resampledData;
}
