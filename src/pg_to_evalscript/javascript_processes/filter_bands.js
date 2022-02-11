function filter_bands(arguments) {
  const { data, bands = [], wavelengths = [] } = arguments;

  if (bands.length === 0 && wavelengths.length === 0) {
    throw new Error(
      "The process `filter_bands` requires any of the parameters `bands`, `common_names` or `wavelengths` to be set."
    );
  }

  if (!data.getDimensionByName(data.bands_dimension_name)) {
    throw new Error("A band dimension is missing.");
  }

  const newData = data.clone();
  newData.filterBands(bands);
  return newData;
}
