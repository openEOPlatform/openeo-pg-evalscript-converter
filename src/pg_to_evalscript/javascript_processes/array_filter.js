function array_filter(arguments) {
  const { data, condition: cond = null, context } = arguments;

  if (data === undefined) {
    throw new Error("Mandatory argument `data` is not defined.");
  }

  if (!Array.isArray(data)) {
    throw new Error("Argument `data` is not an array.");
  }

  if (cond === undefined) {
    throw new Error("Mandatory argument `condition` is not defined.");
  }

  return data.filter((val) => {
    return condition({ x: val });
  });
}
