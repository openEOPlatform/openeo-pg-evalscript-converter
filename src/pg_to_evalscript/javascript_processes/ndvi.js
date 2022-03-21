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

  const newData = data.clone();
  const bandsDim = newData.dimensions.find((d) => d.type === newData.BANDS);
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

  /**
   * calculate NDVI
   */

  if (target_band !== null) {
    bandsDim.labels.push(target_band);
    return newData;
  }

  newData.removeDimension(bandsDim.name);
  return newData;
}
