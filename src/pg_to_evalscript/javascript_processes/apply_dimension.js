function apply_dimension(arguments) {
  const { data, process, dimension, target_dimension = null, context = null } = arguments;

  validateParameter({
    processName: "apply_dimension",
    parameterName: "data",
    value: data,
    nullable: false,
    required: true,
  });

  validateParameter({
    processName: "apply_dimension",
    parameterName: "process",
    value: process,
    nullable: false,
    required: true,
  });

  validateParameter({
    processName: "apply_dimension",
    parameterName: "dimension",
    value: dimension,
    nullable: false,
    required: true,
    allowedTypes: ["string"],
  });

  validateParameter({
    processName: "apply_dimension",
    parameterName: "target_dimension",
    value: target_dimension,
    nullable: true,
    required: false,
    allowedTypes: ["string"],
  });

  validateParameter({
    processName: "apply_dimension",
    parameterName: "context",
    value: context,
    nullable: true,
    required: false,
  });

  const newData = data.clone();
  newData.applyDimension(process, dimension, target_dimension, context);
  return newData;
}
