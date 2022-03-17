function order(arguments) {
  const { data, asc = true, nodata = null} = arguments;

  validateParameter({
    processName: "order",
    parameterName: "data",
    value: data,
    required: true,
    nullable: false,
    array: true,
  });

  validateParameter({
    processName: "order",
    parameterName: "asc",
    value: asc,
    nullable: false,
    allowedTypes: ["boolean"],
  });

  validateParameter({
    processName: "order",
    parameterName: "nodata",
    value: nodata,
    allowedTypes: ["boolean"],
  });

  const dataWithIndex = [];
  for (let i = 0; i < data.length; i++) {
    if (typeof data[i] === "number" || data[i] === null) {
      dataWithIndex.push({ index: i, value: data[i] });
      continue;
    }

    const ISODateString = parse_rfc3339(data[i]);
    if (ISODateString) {
      dataWithIndex.push({ index: i, value: ISODateString.value });
      continue;
    }

    throw new Error("Element in argument `data` is not a number, null or a valid ISO date string.");
  }

  dataWithIndex.sort((a, b) => {
    if (a.value === null && b.value === null) return 0;
    if (a.value === null) return nodata ? 1 : -1;
    if (b.value === null) return nodata ? -1 : 1;

    if (a.value === b.value) return 0;
    if (a.value < b.value) return asc ? -1 : 1;
    if (a.value > b.value) return asc ? 1 : -1;
  });

  const sortedIndexes = [];
  for (let i = 0; i < dataWithIndex.length; i++) {
    if (dataWithIndex[i].value !== null || nodata !== null) {
      sortedIndexes.push(dataWithIndex[i].index);
    }
  }

  return sortedIndexes;
}
