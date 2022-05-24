function resample_cube_temporal(arguments) {
  const { data, target, dimension = null, valid_within = null } = arguments;


  // throw new Error(
  //   "RESAMPLE:____ " + JSON.stringify({
  //     data,
  //     target,
  //   }) +
  //   " ____ RESAMPLE"
  // );

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
  let resampledData = data.clone();
  let temporalDimensionsPairs = [];

  if (dimension) {
    const dataDim = dataClone.getDimensionByName(dimension);
    const targetDim = target.getDimensionByName(dimension);

    // dimension not in one or both datacubes
    if (!dataDim || !targetDim) {
      throw new Error("DimensionNotAvailable");
    }

    if (dataDim.type !== dataClone.TEMPORAL || targetDim !== target.TEMPORAL) {
      throw new Error("DimensionMismatch");
    }

    temporalDimensionsPairs.push({ dataDim, targetDim });
  }
  else {
    for (let targetDimIndex in target.dimensions) {

      targetDimIndex = parseInt(targetDimIndex);
      const targetDim = target.dimensions[targetDimIndex];

      if (targetDim.type === target.TEMPORAL){
        const targetDimSize = target.data.shape[targetDimIndex];

        const dataDimIndex = dataClone.dimensions.findIndex(d => d.name === targetDim.name);
        const dataDim = dataClone.dimensions[dataDimIndex];


        // throw new Error(
        //   "RES ___ " +
        //   JSON.stringify({
        //     dataDim,
        //     targetDim,
        //     dataDimIndex,
        //     targetDimIndex,
        //   }) +
        //   " ___ RES"
        // );

        if (dataDimIndex !== -1 && dataDim.type === dataClone.TEMPORAL) {

          const dataDimSize = dataClone.data.shape[dataDimIndex];

          temporalDimensionsPairs.push({
            dataDim,
            dataDimIndex,
            dataDimSize,
            targetDim,
            targetDimIndex,
            targetDimSize
          });
        }
      }

      
    }

    if (temporalDimensionsPairs.length === 0) {
      throw new Error("DimensionMismatch");
    }
  }


  // go through pairs of dimension that need to be updated
  // ndarray of TARGET not important
  // position of TARGET dimension not important
  for (let pair of temporalDimensionsPairs) {

    let { dataDim, dataDimIndex, dataDimSize, targetDim, targetDimIndex, targetDimSize } = pair;

    let labelIndicesPairs = [];

    let dataToAdd = [];

    // throw new Error(
    //   "DIM LABELS __ " +
    //   JSON.stringify({
    //     pair,
    //     targedDimLabels: targetDim.labels,
    //   }) + 
    //   " ___ DIM LABELS"
    // );

    // go through the TARGET labels and find the nearest SOURCE labels
    // data (ndarray) in the TARGET datacube is not needed
    // determine which data to use for the nearest dates

    resampledData.dimensions[dataDimIndex].labels = [];

    for (let targetLabelIndex in targetDim.labels) {
      targetLabelIndex = parseInt(targetLabelIndex)

      let parsedTargetLabel = new Date(parse_rfc3339(targetDim.labels[targetLabelIndex]).value);
      let minDiff = Number.POSITIVE_INFINITY;
      let minDifParsedDataLabel = null;
      let indexPair = { targetLabelIndex: 0, dataLabelIndex: 0 };


      for (let dataLabelIndex in dataDim.labels) {
        dataLabelIndex = parseInt(dataLabelIndex)

        let parsedDataLabel = new Date(parse_rfc3339(dataDim.labels[dataLabelIndex]).value);
        let diff = Math.abs(parsedDataLabel - parsedTargetLabel);

        if (diff < minDiff) {
          minDiff = diff;
          minDifParsedDataLabel = parsedDataLabel;
          indexPair = { targetLabelIndex, dataLabelIndex };
        }

        // DOCS: The rare case of ties is resolved by choosing the earlier timestamps.
        if(diff === minDiff){
          if (parsedDataLabel < minDifParsedDataLabel){
            minDiff = diff;
            minDifParsedDataLabel = parsedDataLabel;
            indexPair = { targetLabelIndex, dataLabelIndex };
          }
        }
      }
      labelIndicesPairs.push(indexPair);

      // get the values from data's ndarray

      // get the correct subarray by creating and array of nulls with the length of data.shape
      // then replacing the value with the label index at the dimension index

      const shapeArrayWithNullExceptLabelIndex = dataClone.dimensions.map((l, i) => i == dataDimIndex ? indexPair.dataLabelIndex : null )
      
      // PICK THE CORRECT
      const pickedNdarray = dataClone.data.pick(...shapeArrayWithNullExceptLabelIndex);

      const flatPickedNdarray = flattenToNativeArray(pickedNdarray, true);
      dataToAdd.push({ dataDimIndex, indexPair, pickedNdarray, flatPickedNdarray });

      // add to new data
      // resampledData.data


      // throw new Error("flatPickedNdarray " + JSON.stringify({
      //   pickedNdarray,
      //   valuesToAdd: flatPickedNdarray,
      //   dataDimIndex,
      //   finalIndex: indexPair.targetLabelIndex,
      //   shapeArrayWithNullExceptLabelIndex,
      // }));

      // insertIntoDimension() samo dodaja, ne povozi
      // resampledData.insertIntoDimension(dataDimIndex, flatPickedNdarray, indexPair.targetLabelIndex);

      const numOfDims = resampledData.data.shape.length;
      let swappedDims = [...Array(numOfDims).keys()]
      swappedDims[0] = dataDimIndex;
      swappedDims[dataDimIndex] = 0;

      resampledData.data = resampledData.data.transpose(...swappedDims);

      // throw new Error(
      //   "RES ___ " +
      //   JSON.stringify({
      //     dataDimIndex,
      //     numOfDims,
      //     swappedDims,
      //     targetDimSize,
      //     resampledData,
      //   }) +
      //   " ___ RES"
      // );


      // če ne transponiraš, spremeni na pravem mestu
      // resampledData.data.shape[dataDimIndex] = targetDimSize;

      resampledData.data.shape[0] = targetDimSize;

      // moraš posodobit še stride, zato da transpose pravilno dela ...

      // stride se ne posodobi pravilno, tako da ustvari nov ndarray s placeholder podatki
      // in potem dodajaj noter podatke iz dataClone.data

      // ALI

      // TRANSPOSE so that the current temporal dim is always the most outer one

      // zamenjaj ničto in dataDimIndex-to dimenzijo (s ndarray.transpose()),
      // spremeni shape
      // dodaj podatke
      // spet zamenjaj ničto in dataDimIndex-to dimenzijo (s ndarray.transpose()),

      /*
       setInDimension(
          axis [which index in ndarray.shape],
          dataToSet [array],
          index [in the selectedAxis]
        )
      */
      
      // če ne transponiraš, spremeni na pravem mestu
      // resampledData.setInDimension(dataDimIndex, flatPickedNdarray, indexPair.targetLabelIndex);

      resampledData.setInDimension(0, flatPickedNdarray, indexPair.targetLabelIndex);

      // ali je to nujno ?????
      resampledData.data = ndarray(flattenToNativeArray(resampledData.data, true), resampledData.data.shape);
      
      // transpose back
      resampledData.data = resampledData.data.transpose(...swappedDims);

      resampledData.dimensions[dataDimIndex].labels[indexPair.targetLabelIndex] = dataDim.labels[indexPair.dataLabelIndex];


      // throw new Error(
      //   "RES ___ " +
      //   JSON.stringify({
      //     dataDimIndex,
      //     numOfDims,
      //     swappedDims,
      //     flatPickedNdarray,
      //     resampledData,
      //     flat: flattenToNativeArray(resampledData.data, true) 
      //   }) +
      //   " ___ RES"
      // );

    }

    // REMOVE not overwritten lines in data
    resampledData.data = ndarray(flattenToNativeArray(resampledData.data, true), resampledData.data.shape);

    

    // throw new Error(
    //   "RES ___ " +
    //   JSON.stringify({
    //     data,
    //     target,
    //     datadim: dataDim.name,
    //     dataDimIndex,
    //     dataDimSize,
    //     labelIndicesPairs,
    //     dataToAdd,
    //     resampledData,
    //     flat: flattenToNativeArray(resampledData.data, true),
    //   }) +
    //   " ___ RES"
    // );

  }


  // throw new Error(
  //   "RES ___ " +
  //   JSON.stringify({
  //     data,
  //     target,
  //     // temporalDimensionsPairs,
  //     resampledData,
  //   }) +
  //   " ___ RES"
  // );





  // last step - update the labels for the returned DataCube
  // for (let pair of temporalDimensionsPairs) {
  //   let { dataDim, targetDim } = pair;
  //   dataDim.labels = targetDim.labels;
  // }

  // update the ndarray data for the returned DataCube
  // we can't just clone target data (ndarray) because the dimensions might not be in the same order!
  // dataClone.data = target.data.slice();

  // find the nearest dates and change the vals in returned DataCube

  // valid_within param: 
  // getFilteredTemporalIndices(..., [date in data] - valid_within, [date in data] + valid_within)


  // throw new Error(
  //   "RESAMPLE:____ " + JSON.stringify({
  //     data,
  //     target,
  //     resampledData
  //   }) +
  //   " ____ RESAMPLE"
  // )

  return resampledData;
}
