function aggregate_temporal_period(arguments) {
  const startTime = Date.now();
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
  newData.aggregateTemporalPeriod(period, reducer, dimension, context);
  const endTime = Date.now();
  executionTimes.push({ fun: "aggregate_temporal_period.js", params: {period, dimension}, success: true, time: endTime - startTime });
  return newData;
}
