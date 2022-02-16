function min(arguments) {
  const { data, ignore_nodata = true } = arguments;
  if (!data || data.length === 0 || (!ignore_nodata && data.includes(null))) {
    return null;
  }
  return Math.min(...data.filter((i) => i !== null && i !== undefined));
}
