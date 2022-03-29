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

  // check that each dimension, present in both data and mask,
  // have the same: name, type, reference system, resolution and labels


  // for (let dimension of cube1.dimensions) {
  //   const dimension2 = cube2.getDimensionByName(dimension.name);

  //   if (!dimension2) {
  //     throw new Error(`dimension \`${dimension.name}\` from argument \`data\` not in argument \`mask\`.`);
  //   }

  //   if (dimension.type !== dimension2.type){
  //     throw new Error(`dimension \`${dimension.name}\` from argument \`data\` not of same type as in argument \`mask\`.`);
  //   }

  //   if (dimension.labels.length !== dimension2.labels.length || dimension.labels.every((l) => dimension2.labels.includes(l))) {
  //     throw new Error(`labels for dimension \`${dimension.name}\` from argument \`data\` not same as in argument \`mask\`.`);
  //   }

  // }


  // replace pixel in data if the corresponding pixel in mask is
  // non-zero (for numbers) or true (for boolean values)

  let newData = data.clone();

  let flatData = newData.flattenToArray();
  let flatMask = mask.flattenToArray();
  const replacement_val = replacement === undefined ? null : replacement;

  // console.log('data within json', JSON.stringify({
  //   data
  //   // d: newData.data,
  //   // flatData, 
  //   // flatMask
  // }));


  for(let i=0; i<flatData.length; i++){
    const shouldBeReplaced = (typeof flatMask[i] === 'number' && flatMask[i] !== 0) || (typeof flatMask[i] === 'boolean' && flatMask[i] === true);
    if(shouldBeReplaced){
      flatData[i] = replacement_val;
    }
  }




  return newData;
}
