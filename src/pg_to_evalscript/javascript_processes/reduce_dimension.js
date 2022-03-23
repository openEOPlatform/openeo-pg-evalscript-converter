function reduce_dimension(arguments) {
  const { data, dimension, reducer } = arguments;

  validateParameter({
    processName: "reduce_dimension",
    parameterName: "data",
    value: data,
    nullable: false,
    required: true,
  });

  validateParameter({
    processName: "reduce_dimension",
    parameterName: "dimension",
    value: dimension,
    nullable: false,
    required: true,
    allowedTypes: ["string"],
  });

  validateParameter({
    processName: "reduce_dimension",
    parameterName: "reducer",
    value: reducer,
    nullable: false,
    required: true,
  });

  const newData = data.clone();
  newData.reduceByDimension(reducer, dimension);
  return newData;
}
