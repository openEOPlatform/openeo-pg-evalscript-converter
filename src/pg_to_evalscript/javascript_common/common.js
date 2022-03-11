function parse_rfc3339(dt, default_h = 0, default_m = 0, default_s = 0) {
  const regexDateTime =
    "^([0-9]{4})-([0-9]{2})-([0-9]{2})([Tt]([0-9]{2}):([0-9]{2}):([0-9]{2})(\\.[0-9]+)?)?(([Zz]|([+-])([0-9]{2}):([0-9]{2})))?";
  const regexDate = "^([0-9]{4})-([0-9]{2})-([0-9]{2})$";

  let result = null;

  try {
    const g = dt.match(regexDateTime);
    if (g) {
      let date = Date.UTC(
        parseInt(g[1]), //year
        parseInt(g[2]) - 1, // month
        parseInt(g[3]), //day
        parseInt(g[5] || default_h), //hour
        parseInt(g[6] || default_m), //minute
        parseInt(g[7] || default_s), // second
        parseFloat(g[8]) * 1000 || 0 // milisecond
      );

      //for date-time strings either time zone or Z should be provided
      if (g[5] !== undefined && g[9] === undefined) {
        return null;
      }

      //check if timezone is provided
      if (g[9] !== undefined && g[9] !== "Z") {
        //offset in minutes
        const offset =
          (parseInt(g[12] || 0) * 60 + parseInt(g[13] || 0)) *
          (g[11] === "+" ? -1 : 1);
        //add offset in miliseconds
        date = date + offset * 60 * 1000;
      }

      return {
        type: dt.match(regexDate) ? "date" : "date-time",
        value: new Date(date).toISOString(),
      };
    }
  } catch (err) {
    //
  }

  return result;
}

class ProcessError extends Error {
  constructor({ name, message }) {
    super(message);
    this.name = name;
  }
}

class ValidationError extends Error {
  constructor({ name, message }) {
    super(message);
    this.name = name;
  }
}

const VALIDATION_ERRORS = {
  MISSING_PARAMETER: "MISSING_PARAMETER",
  WRONG_TYPE: "WRONG_TYPE",
  NOT_NULL: "NOT_NULL",
  NOT_ARRAY: "NOT_ARRAY",
  NOT_INTEGER: "NOT_INTEGER",
  NOT_BOOLEAN: "NOT_BOOLEAN",
  MIN_VALUE: "MIN_VALUE",
  MAX_VALUE: "MAX_VALUE",
};

function validateParameter(arguments) {
  const {
    processName,
    parameterName,
    value,
    required = false,
    nullable = true,
    allowedTypes,
    array,
    integer,
    boolean,
    min,
    max,
  } = arguments;

  if (!!required && value === undefined) {
    throw new ValidationError({
      name: VALIDATION_ERRORS.MISSING_PARAMETER,
      message: `Process ${processName} requires parameter ${parameterName}.`,
    });
  }

  if (!nullable && value === null) {
    throw new ValidationError({
      name: VALIDATION_ERRORS.NOT_NULL,
      message: `Value for ${parameterName} should not be null.`,
    });
  }

  if (
    allowedTypes &&
    Array.isArray(allowedTypes) &&
    value !== null &&
    value !== undefined &&
    !allowedTypes.includes(typeof value)
  ) {
    throw new ValidationError({
      name: VALIDATION_ERRORS.WRONG_TYPE,
      message: `Value for ${parameterName} is not a ${allowedTypes.join(
        " or a "
      )}.`,
    });
  }

  if (array && !Array.isArray(value)) {
    throw new ValidationError({
      name: VALIDATION_ERRORS.NOT_ARRAY,
      message: `Value for ${parameterName} is not an array.`,
    });
  }

  if (integer && !Number.isInteger(value)) {
    throw new ValidationError({
      name: VALIDATION_ERRORS.NOT_INTEGER,
      message: `Value for ${parameterName} is not an integer.`,
    });
  }

  if (
    boolean &&
    value !== undefined &&
    value !== null &&
    typeof value !== "boolean"
  ) {
    throw new ValidationError({
      name: VALIDATION_ERRORS.NOT_BOOLEAN,
      message: `Value for ${parameterName} is not a boolean.`,
    });
  }

  if (min !== undefined && min !== null && value < min) {
    throw new ValidationError({
      name: VALIDATION_ERRORS.MIN_VALUE,
      message: `Value for ${parameterName} must be greater or equal to ${min}.`,
    });
  }

  if (max !== undefined && max !== null && value > max) {
    throw new ValidationError({
      name: VALIDATION_ERRORS.MAX_VALUE,
      message: `Value for ${parameterName} must be less or equal to ${max}.`,
    });
  }

  return true;
}
