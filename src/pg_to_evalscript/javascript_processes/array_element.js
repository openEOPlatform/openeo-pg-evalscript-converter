function array_element(arguments) {
  const { data, labels, index, label, return_nodata = false } = arguments;
  if (!data.labels) {
    data.labels = labels;
  }
  if (index === undefined && label === undefined) {
    throw "The process `array_element` requires either the `index` or `labels` parameter to be set.";
  }
  if (index !== undefined && label !== undefined) {
    throw "The process `array_element` only allows that either the `index` or the `labels` parameter is set.";
  }
  if (index !== undefined) {
    if (data.length <= index) {
      if (return_nodata) {
        return null;
      }
      throw "The array has no element with the specified index or label.";
    }
    return data[index];
  }
  if (data.labels === undefined) {
    throw "The array is not a labeled array, but the `label` parameter is set. Use the `index` instead.";
  }
  if (!data.labels.includes(label)) {
    if (return_nodata) {
      return null;
    }
    throw "The array has no element with the specified index or label.";
  }
  return data[data.labels.indexOf(label)];
}
