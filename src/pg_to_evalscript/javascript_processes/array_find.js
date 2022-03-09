function array_find(arguments) {
  const { data, value } = arguments;
  if (data === null || data === undefined) {
    throw new Error("Mandatory argument `data` is either null or not defined.");
  }
  if (!Array.isArray(data)) {
    throw new Error("Argument `data` is not an array.");
  }
  if (value === undefined) {
    throw new Error("Mandatory argument `value` is not defined.");
  }

  if (typeof value === "object" || value === null) {
    return null;
  }
  const index = data.findIndex((x) => x === value);
  
  return (index === -1 ? null : index);
}
