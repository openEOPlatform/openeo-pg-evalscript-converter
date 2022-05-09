function mask(arguments) {
  const { data, mask, replacement = null } = arguments;

  validateParameter({
    processName: "mask",
    parameterName: "data",
    value: data,
    required: true,
  });

  validateParameter({
    processName: "mask",
    parameterName: "mask",
    value: mask,
    required: true,
  });

  validateParameter({
    processName: "mask",
    parameterName: "replacement",
    value: replacement,
    required: false,
    allowedTypes: ["number", "boolean", "string"],
  });

  // The data cubes have to be compatible so that each dimension in the mask 
  // must also be available in the raster data cube with the same
  // name, type, reference system, resolution and labels.

  // check that each dimension, present in mask
  // - is present in data
  // - has the same:
  //    - name, (taken care of by searching for dimension by name)
  //    - type,
  //    - reference system, (not sure how to check that)
  //    - resolution, (not sure how to check that)
  //    - labels

  for (let maskDim of mask.dimensions) {
    const dataDim = data.getDimensionByName(maskDim.name);

    if (!dataDim) {
      throw new Error(`Dimension \`${maskDim.name}\` from argument \`mask\` not in argument \`data\`.`);
    }

    if (maskDim.type !== dataDim.type) {
      throw new Error(`Type of the dimension \`${maskDim.name}\` from argument \`mask\` is not the same as in argument \`data\`.`);
    }

    if (maskDim.labels.length !== dataDim.labels.length || !maskDim.labels.every((l) => dataDim.labels.includes(l))) {
      throw new Error(`Labels for dimension \`${maskDim.name}\` from argument \`mask\` are not the same as in argument \`data\`.`);
    }
  }

  let newData = data.clone();
  let newDataFlat = newData.flattenToArray();

  // broadcast the mask parameter's ndarray to match the data parameter's ndarray
  const maskBroadcasted = broadcastNdarray(mask.data, newData.data.shape);
  const maskBroadcastedFlat = flattenToNativeArray(maskBroadcasted);

  const replacement_val = replacement === undefined ? null : replacement;

  // replace pixel in data if the corresponding pixel in mask is
  // non-zero (for numbers) or true (for boolean values)
  for (let i = 0; i < newDataFlat.length; i++) {
    const maskElNumber = (typeof maskBroadcastedFlat[i] === 'number' && maskBroadcastedFlat[i] !== 0);
    const maskElBool = (typeof maskBroadcastedFlat[i] === 'boolean' && maskBroadcastedFlat[i] === true);
    const shouldBeReplaced = maskElNumber || maskElBool;
    if (shouldBeReplaced) {
      newDataFlat[i] = replacement_val;
    }
  }

  return newData;
}
