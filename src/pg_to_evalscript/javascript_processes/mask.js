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

  // NAČIN 1
  // najprej obstoječe dimenzije v mask daj v "isti" vrstni red kot v data
  // potem dodaj manjkajoče dimenzije 

  // NAČIN 2 - uporabljen
  // najprej dodaj manjkajoče dimenzije (na začetek)
  // potem spremeni vrstni red mask, da bo enak kot v data

  let maskWithMissingDims = mask.clone();
  for (let dataDim of data.dimensions) {
    if (!maskWithMissingDims.getDimensionByName(dataDim.name)) {
      maskWithMissingDims.addDimension(dataDim.name, "label to be removed", dataDim.type);
      maskWithMissingDims.setDimensionLabels(dataDim.name, []);
    }
  }

  // use THIS to get the correct order of the dimensions
  // then transpose the data matrix!!!

  // let dimensionsOrder = [];
  let dimsOrd = []
  for (let dataDimIndex in data.dimensions) {
    const dataDim = data.dimensions[parseInt(dataDimIndex)];
    const maskDimIndex = maskWithMissingDims.dimensions.findIndex((d) => d.name === dataDim.name);

    // add to mask

    if (maskDimIndex === -1) {
      throw new Error("AAAAAAAAAAAAAAAAAAAAAAAA" + JSON.stringify({
        dataDimIndex,
        maskDimIndex,
        dataDim
      }));
    }

    // dimensionsOrder.push({
    //   wantedIndex: parseInt(dataDimIndex),
    //   currentIndex: maskDimIndex
    // });
    dimsOrd.push(maskDimIndex);
  }


  // data, bands_dimension_name, temporal_dimension_name, fromSamples, bands_metadata, scenes
  let correctedMaskWithDims = maskWithMissingDims.clone();

  correctedMaskWithDims.data = correctedMaskWithDims.data.transpose(...dimsOrd);

  // fix order of dimensions for the correctedMaskWithDims Datacube

  const dimensionsOldOrder = correctedMaskWithDims.dimensions.slice();
  correctedMaskWithDims.dimensions = dimsOrd.map(val => dimensionsOldOrder[val]);

  // broadcast correctedMaskWithDims.data
  // let newData2 = data.clone();
  // const maskBroadcasted2 = broadcastNdarray(correctedMaskWithDims.data, newData2.data.shape);

  // then it's ready for masking

  // throw new Error(
  //   "MISSING ___ " + 
  //   JSON.stringify({
  //     mask,
  //     // data,
  //     maskWithMissingDims,
  //     correctedMaskWithDims,
  //     maskBroadcasted2,
  //     // dimensionsOrder,
  //     // dimsOrd,
  //   }) + 
  //   " ___ MISSING"
  // );

  let newData = data.clone();
  let newDataFlat = newData.flattenToArray();

  const maskBroadcasted = broadcastNdarray(correctedMaskWithDims.data, newData.data.shape);
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

  // throw new Error(
  //   "EEE ___ " +
  //   JSON.stringify({
  //     data,
  //     mask,
  //     newData,
  //   }) +
  //   " ___ EEE"
  // );

  return newData;
}
