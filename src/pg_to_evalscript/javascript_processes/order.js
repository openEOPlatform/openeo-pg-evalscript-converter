function order(arguments) {
  const { data, asc = true, nodata = null} = arguments;

  if (data === null || data === undefined) {
    throw new Error("Mandatory argument `data` is either null or not defined.");
  }

  if (!Array.isArray(data)) {
    throw new Error("Argument `data` is not an array.");
  }

  if (typeof asc !== "boolean") {
    throw new Error("Argument `asc` is not a boolean.");
  }

  if (typeof nodata !== "boolean" && nodata !== null) {
    throw new Error("Argument `asc` is not a boolean or null.");
  }

  return data
    .map((value, index) => {
      return { value, index };
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
