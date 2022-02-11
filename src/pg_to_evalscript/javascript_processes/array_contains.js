function array_contains(arguments) {
  const { data, value } = arguments;
  if (typeof value === "object" || value === null) {
    return false;
  }
  const el = Array.from(data).find((x) => x === value);
  return typeof el === typeof value;
}
