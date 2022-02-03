function mean(arguments) {
  const { data, ignore_nodata = true } = arguments;
  if (
    (!ignore_nodata && data.includes(null)) ||
    data.length === 0 ||
    data.every((i) => i === null)
  ) {
    return null;
  }
  return (
    data.reduce((prev, curr) => prev + curr) /
    data.filter((i) => i !== null).length
  );
}
