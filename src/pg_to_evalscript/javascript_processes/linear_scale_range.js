function linear_scale_range(arguments) {
  const { x, inputMin, inputMax, outputMin = 0, outputMax = 1 } = arguments;

  if (x === null || x === undefined) {
    return null;
  }

  if (inputMin === null || inputMin === undefined) {
    throw Error("Process linear_scale_range requires argument inputMin.");
  }

  if (inputMax === null || inputMax === undefined) {
    throw Error("Process linear_scale_range requires argument inputMax.");
  }

  //The given number in x is clipped to the bounds specified in inputMin and inputMax
  const clippedValue = Math.min(inputMax, Math.max(x, inputMin));

  return (
    ((clippedValue - inputMin) / (inputMax - inputMin)) *
      (outputMax - outputMin) +
    outputMin
  );
}
