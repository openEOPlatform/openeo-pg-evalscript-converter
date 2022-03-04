function filter_bands(arguments) {
  const { data, bands = [], wavelengths = [] } = arguments;

  if (data === undefined) {
    throw new Error("Mandatory argument `data` is not defined.");
  }

  if (!Array.isArray(bands)) {
    throw new Error("Argument `bands` is not an array.");
  }

  if (!Array.isArray(wavelengths)) {
    throw new Error("Argument `wavelengths` is not an array.");
  }

  if (bands.length === 0 && wavelengths.length === 0) {
    throw new Error(
      "The process `filter_bands` requires any of the parameters `bands`, `common_names` or `wavelengths` to be set."
    );
  }

  if (!bands.every((e) => typeof e === "string")) {
    throw new Error("Element in argument `bands` is not a string.");
  }

  if (!data.getDimensionByName(data.bands_dimension_name)) {
    throw new Error("A band dimension is missing.");
  }

  const newData = data.clone();
  newData.filterBands(bands);
  return newData;
}
