function aggregate_temporal_period(arguments) {
  const formatLabelByPeriod = (periodType, label) => {
    const dayInYear = (date) => {
      return (
        (Date.UTC(date.getFullYear(), date.getMonth(), date.getDate()) -
          Date.UTC(date.getFullYear(), 0, 0)) /
        24 /
        60 /
        60 /
        1000
      );
    };

    const dekadInYear = (date) => {
      const monthCount = date.getMonth();
      const dekadCount = Math.floor((date.getDate() - 1) / 10) + 1;
      return monthCount * 3 + (dekadCount > 2 ? 3 : dekadCount);
    };

    const padWithZeros = (num, size) => {
      num = num.toString();
      while (num.length < size) {
        num = "0" + num;
      }
      return num;
    };

    const d = new Date(parse_rfc3339(label).value);
    switch (periodType) {
      case "hour":
        const hourCount = d.getHours();
        const days = d.getDate();
        const months = d.getMonth() + 1;
        return `${d.getFullYear()}-${padWithZeros(months, 2)}-${padWithZeros(
          days,
          2
        )}-${padWithZeros(hourCount, 2)}`;
      case "day":
        const dayCount = dayInYear(d);
        return `${d.getFullYear()}-${padWithZeros(dayCount, 3)}`;
      case "week":
        const weekCount = Math.ceil(dayInYear(d) / 7);
        return `${d.getFullYear()}-${padWithZeros(weekCount, 2)}`;
      case "dekad":
        const dekadCount = dekadInYear(d);
        return `${d.getFullYear()}-${padWithZeros(dekadCount, 2)}`;
      case "month":
        const monthCount = d.getMonth() + 1;
        return `${d.getFullYear()}-${padWithZeros(monthCount, 2)}`;
      case "season":
        const month = d.getMonth() + 1;
        let seasonName = null;
        if (month >= 3 && month <= 5) {
          seasonName = "mam";
        } else if (month >= 6 && month <= 8) {
          seasonName = "jja";
        } else if (month >= 9 && month <= 11) {
          seasonName = "son";
        } else {
          seasonName = "djf";
        }
        return `${d.getFullYear()}-${seasonName}`;
      case "tropical-season":
        let tropicalSeasonName = null;
        if (d.getMonth() + 1 >= 5 && d.getMonth() + 1 <= 10) {
          tropicalSeasonName = "mjjaso";
        } else {
          tropicalSeasonName = "ndjfma";
        }
        return `${d.getFullYear()}-${tropicalSeasonName}`;
      case "year":
        return `${d.getFullYear()}`;
      case "decade":
        return `${d.getFullYear().toString().substring(0, 3)}0`;
      case "decade-ad":
        return `${d.getFullYear().toString().substring(0, 3)}1`;
      default:
        throw new ProcessError({
          name: "UnknownPeriodValue",
          message: `Value '${periodType}' is not an allowed value for period.`,
        });
    }
  };

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

  // add code for aggregating
  const axis = newData.dimensions.findIndex(
    (d) => (d.name = temporalDimensionToAggregate.name)
  );
  const newLabels = [];
  const newValues = [];
  for (let label of temporalDimensionToAggregate.labels) {
    newLabels.push(formatLabelByPeriod(period, label));

    const allCoords = newData._iterateCoords(newData.data.shape.slice(), [
      axis,
    ]);

    for (let coords of allCoords) {
      const dataToReduce = convert_to_1d_array(
        newData.data.pick.apply(newData.data, coords)
      );

      const newVals = reducer({
        data: dataToReduce,
        context: context,
      });
      newValues.push(newVals);
    }
  }

  temporalDimensionToAggregate.labels = newLabels;
  const newShape = newData.getDataShape().slice();
  newShape[axis] = newLabels.length;
  newData.data = ndarray(newValues, newShape);

  return newData;
}
