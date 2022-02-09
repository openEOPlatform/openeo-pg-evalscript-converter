function sum(arguments) {
  const { data, ignore_nodata = true } = arguments;

  if (!data || data.length === 0 || (!ignore_nodata && data.includes(null))) {
    return null;
  }

  return data.reduce((acc, curr) => acc + curr);
}
