function aggregate_temporal(arguments) {
  const { data, intervals, reducer, labels = [], dimension = null, context = null } = arguments;

  const newData = data.clone();
  newData.aggregateTemporal(intervals, reducer, labels, dimension, context);
  return newData;
}
