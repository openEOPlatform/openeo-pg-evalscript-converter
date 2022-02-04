function max(arguments) {
  const { data, ignore_nodata = true } = arguments;
  if ((!ignore_nodata && data.includes(null)) || data.length === 0) {
    return null;
  }
  return Math.max(...data.filter((i) => i !== null));
}
