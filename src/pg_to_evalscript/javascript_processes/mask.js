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

  // add missing dimensions (as labelless dimensions of length 1) at the start of mask's dimensions
  let maskWithMissingDims = mask.clone();
  for (let dataDim of data.dimensions) {
    if (!maskWithMissingDims.getDimensionByName(dataDim.name)) {
      maskWithMissingDims.addDimension(dataDim.name, "label to be removed", dataDim.type);
      maskWithMissingDims.setDimensionLabels(dataDim.name, []);
    }
  }

  // get the correct order for mask's dimensions
  let dimensionsOrder = [];
  for (let dataDim of data.dimensions) {
    dimensionsOrder.push(maskWithMissingDims.dimensions.findIndex((d) => d.name === dataDim.name));
  }

  // fix the order of mask's dimensions
  const dimensionsOldOrder = maskWithMissingDims.dimensions.slice();
  maskWithMissingDims.dimensions = dimensionsOrder.map(val => dimensionsOldOrder[val]);

  // transpose mask's ndarray to be in sync with the order of the dimensions
  maskWithMissingDims.data = maskWithMissingDims.data.transpose(...dimensionsOrder);

  let newData = data.clone();
  let newDataFlat = newData.flattenToArray();

  // broadcast the mask's ndarray to the size of data's ndarray
  const maskBroadcasted = broadcastNdarray(maskWithMissingDims.data, newData.data.shape);
  const maskBroadcastedFlat = flattenToNativeArray(maskBroadcasted, true);

  const replacement_val = replacement === undefined ? null : replacement;

  for (let i = 0; i < newDataFlat.length; i++) {
    const maskElNumber = (typeof maskBroadcastedFlat[i] === 'number' && maskBroadcastedFlat[i] !== 0);
    const maskElBool = (typeof maskBroadcastedFlat[i] === 'boolean' && maskBroadcastedFlat[i] === true);
    const shouldBeReplaced = maskElNumber || maskElBool;
    if (shouldBeReplaced) {
      newDataFlat[i] = replacement_val;
    }
  }
  
  newData.data.data = newDataFlat;
  return newData;
}
