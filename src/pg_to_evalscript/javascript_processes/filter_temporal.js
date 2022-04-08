function filter_temporal(arguments) {
  const { data, extent, dimension } = arguments;

  validateParameter({
    processName: "filter_temporal",
    parameterName: "data",
    value: data,
    required: true,
    nullable: false,
  });

  validateParameter({
    processName: "filter_temporal",
    parameterName: "extent",
    value: extent,
    required: true,
    nullable: false,
    array: true,
  });

  validateParameter({
    processName: "filter_temporal",
    parameterName: "dimension",
    value: dimension,
    required: false,
    nullable: true,
    allowedTypes: ["string"],
  });

  const newData = data.clone();
  newData.filterTemporal(extent, dimension);
  return newData;
}
