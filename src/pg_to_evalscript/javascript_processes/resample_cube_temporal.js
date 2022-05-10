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


  let resampledData = data.clone();
  let temporalDimensionsPairs = [];

  if (dimension) {
    const dataDim = resampledData.getDimensionByName(dimension);
    const targetDim = target.getDimensionByName(dimension);

    // dimension not in one or both datacubes
    if (!dataDim || !targetDim) {
      throw new Error("DimensionNotAvailable");
    }

    if (dataDim.type !== resampledData.TEMPORAL || targetDim !== target.TEMPORAL) {
      throw new Error("DimensionMismatch");
    }

    temporalDimensionsPairs.push({ dataDim, targetDim });
  }
  else {
    // don't throw an error when searching for temporal dimensions
    // throw an error that is defined for the process in case of no matching temporal dimensions
    try {
      const dataDims = resampledData.getTemporalDimensions();
      const targetDims = target.getTemporalDimensions();

      for (let dataDim of dataDims) {
        const targetDim = targetDims.find(d => d.name === dataDim.name);
        if (targetDim) {
          temporalDimensionsPairs.push({ dataDim, targetDim });
        }
      }

      if (temporalDimensionsPairs.length === 0) {
        throw new Error("DimensionMismatch");
      }
    }
    catch (e) {
      throw new Error("DimensionMismatch");
    }
  }

  // update the labels for the returned DataCube
  // for (let pair of temporalDimensionsPairs) {
  //   let { dataDim, targetDim } = pair;
  //   dataDim.labels = targetDim.labels;
  // }

  // update the ndarray data for the returned DataCube


  // throw new Error(
  //   "RESAMPLE:____ " + JSON.stringify({
  //     data,
  //     target,
  //     resampledData,
  //   }) +
  //   " ____ RESAMPLE"
  // )

  return resampledData;
}
