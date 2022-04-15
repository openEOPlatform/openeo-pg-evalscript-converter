function aggregate_temporal(arguments) {
  const { data, intervals, reducer, labels = [], dimension = null, context = null } = arguments;

  validateParameter({
    processName: "aggregate_temporal",
    parameterName: "data",
    value: data,
    required: true,
    nullable: false,
  });

  validateParameter({
    processName: "aggregate_temporal",
    parameterName: "intervals",
    value: intervals,
    required: true,
    nullable: false,
    array: true,
  });

  validateParameter({
    processName: "aggregate_temporal",
    parameterName: "reducer",
    value: reducer,
    required: true,
    nullable: false,
  });

  validateParameter({
    processName: "aggregate_temporal",
    parameterName: "labels",
    value: labels,
    required: false,
    nullable: false,
    array: true,
  });

  validateParameter({
    processName: "aggregate_temporal",
    parameterName: "dimension",
    value: dimension,
    required: false,
    nullable: true,
    allowedTypes: ["string"],
  });

  validateParameter({
    processName: "aggregate_temporal",
    parameterName: "context",
    value: context,
    required: false,
    nullable: true,
  });

  const newData = data.clone();
  newData.aggregateTemporal(intervals, reducer, labels, dimension, context);
  return newData;
}
