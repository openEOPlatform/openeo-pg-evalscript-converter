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
  let flatData = newData.flattenToArray();
  let flatMask = mask.flattenToArray();
  const replacement_val = replacement === undefined ? null : replacement;

  // replace pixel in data if the corresponding pixel in mask is
  // non-zero (for numbers) or true (for boolean values)
  for (let i = 0; i < flatData.length; i++) {
    const shouldBeReplaced = (typeof flatMask[i] === 'number' && flatMask[i] !== 0) || (typeof flatMask[i] === 'boolean' && flatMask[i] === true);
    if (shouldBeReplaced) {
      flatData[i] = replacement_val;
    }
  }

  return newData;
}
