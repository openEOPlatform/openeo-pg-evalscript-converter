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

  // The data and mask cubes have to be compatible, meaning each dimension in the mask must also be
  // available in the data cube with the same name, type, reference system, resolution and labels.

  // check that each dimension, present in mask
  // - is also present in data
  // - has the same:
  //    - name (taken care of by searching for dimension by name)
  //    - type
  //    - labels
  //    - reference system (no check yet)
  //    - resolution (no check yet)

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

  const maskBroadcasted = broadcastNdarray(mask.data, newData.data.shape);
  const maskBroadcastedFlat = flattenToNativeArray(maskBroadcasted);

  const replacement_val = replacement === undefined ? null : replacement;

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
