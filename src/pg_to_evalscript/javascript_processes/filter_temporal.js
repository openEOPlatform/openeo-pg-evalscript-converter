function filter_temporal(arguments) {
  const { data, extent, dimension } = arguments;

  const newData = data.clone();
  newData.filterTemporal(extent, dimension);
  return newData;
}
