function aggregate_temporal_period(arguments) {
  const { data, period, reducer, dimension = null, context = null } = arguments;

  validateParameter({
    processName: "aggregate_temporal_period",
    parameterName: "data",
    value: data,
    nullable: false,
    required: true,
  });

  validateParameter({
    processName: "aggregate_temporal_period",
    parameterName: "period",
    value: period,
    nullable: false,
    required: true,
    allowedTypes: ["string"],
  });

  validateParameter({
    processName: "aggregate_temporal_period",
    parameterName: "reducer",
    value: reducer,
    nullable: false,
    required: true,
  });

  validateParameter({
    processName: "aggregate_temporal_period",
    parameterName: "dimension",
    value: dimension,
    allowedTypes: ["string"],
  });

  validateParameter({
    processName: "aggregate_temporal_period",
    parameterName: "context",
    value: context,
  });

  const newData = data.clone();
  const temporalDimensions = newData.dimensions.filter(
    (d) => d.type === newData.TEMPORAL
  );
  if (!dimension && temporalDimensions.length > 1) {
    throw new ProcessError({
      name: "TooManyDimensions",
      message:
        "The data cube contains multiple temporal dimensions. The parameter `dimension` must be specified.",
    });
  }

  const temporalDimensionToAggregate = dimension
    ? temporalDimensions.find((d) => d.name === dimension)
    : temporalDimensions[0];
  if (!temporalDimensionToAggregate) {
    throw new ProcessError({
      name: "DimensionNotAvailable",
      message: "A dimension with the specified name does not exist.",
    });
  }

  // 1 more exception to handle DistinctDimensionLabelsRequired
  // add code for aggregating

  return newData;
}
