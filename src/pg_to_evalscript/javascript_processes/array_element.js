function array_element(arguments) {
  const { data, index, label, return_nodata = false } = arguments;

  if (data === null || data === undefined) {
    throw new Error("Mandatory argument `data` is either null or not defined.");
  }

  if (index === undefined && label === undefined) {
    throw new Error(
      "The process `array_element` requires either the `index` or `labels` parameter to be set."
    );
  }

  if (index !== undefined && label !== undefined) {
    throw new Error(
      "The process `array_element` only allows that either the `index` or the `labels` parameter is set."
    );
  }

  if (index !== undefined) {
    if (!Number.isInteger(index)) {
      throw new Error("Argument `index` is not an integer.");
    }

    if (data.length <= index) {
      if (return_nodata) {
        return null;
      }
      throw new Error(
        "The array has no element with the specified index or label."
      );
    }
    return data[index];
  }

  if (data.labels === undefined) {
    throw new Error(
      "The array is not a labeled array, but the `label` parameter is set. Use the `index` instead."
    );
  }

  if (typeof label !== "string" && typeof label !== "number") {
    throw new Error("Argument `label` is not a string or a number.");
  }

  if (!data.labels.includes(label)) {
    if (return_nodata) {
      return null;
    }
    throw new Error(
      "The array has no element with the specified index or label."
    );
  }

  return data[data.labels.indexOf(label)];
}
