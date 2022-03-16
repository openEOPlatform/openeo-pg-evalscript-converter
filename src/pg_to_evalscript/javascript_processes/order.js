function order(arguments) {
  const { data, asc = true, nodata = null} = arguments;

  validateParameter({
    processName: "order",
    parameterName: "data",
    value: data,
    required: true,
    array: true,
  });

  validateParameter({
    processName: "order",
    parameterName: "asc",
    value: asc,
    required: true,
    nullable: false,
    allowedTypes: ["boolean"],
  });

  validateParameter({
    processName: "nodata",
    parameterName: "nodata",
    value: nodata,
    required: true,
    allowedTypes: ["boolean"],
  });

  return data
    .map((value, index) => {
      if (typeof value === "number" || value === null) {
        return { value, index };
      }

      const ISODateString = parse_rfc3339(value);
      if (ISODateString) {
        return { value: ISODateString.value, index };
      }

      throw new Error("Element in argument `data` is not a number, null or a valid ISO date string.");
    })
    .sort((a, b) => {
      if (a.value === null && b.value === null) return 0;
      if (a.value === null) return nodata ? 1 : -1;
      if (b.value === null) return nodata ? -1 : 1;

      if (a.value === b.value) return 0;
      if (a.value < b.value) return asc ? -1 : 1;
      if (a.value > b.value) return asc ? 1 : -1;
    })
    .filter(obj => {
      return obj.value !== null || nodata !== null;
    })
    .map(obj => obj.index);
}
