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

const formatLabelByPeriod = (period, label) => {
  const dayInYear = (date) => {
    return (
      (Date.UTC(date.getFullYear(), date.getMonth(), date.getDate()) -
        Date.UTC(date.getFullYear(), 0, 0)) /
      24 /
      60 /
      60 /
      1000
    );
  };

  const dekadInYear = (date) => {
    const monthCount = date.getMonth();
    const dekadCount = Math.floor((date.getDate() - 1) / 10) + 1;
    return monthCount * 3 + (dekadCount > 2 ? 3 : dekadCount);
  };

  const padWithZeros = (num, size) => {
    num = num.toString();
    while (num.length < size) {
      num = "0" + num;
    }
    return num;
  };

  const d = new Date(label);
  switch (period) {
    case "hour":
      const hourCount = d.toISOString().split("T")[1].substring(0, 2);
      const days = d.getDate();
      const months = d.getMonth() + 1;
      return `${d.getFullYear()}-${padWithZeros(months, 2)}-${padWithZeros(
        days,
        2
      )}-${hourCount}`;
    case "day":
      const dayCount = dayInYear(d);
      return `${d.getFullYear()}-${padWithZeros(dayCount, 3)}`;
    case "week":
      const weekCount = Math.ceil(dayInYear(d) / 7);
      return `${d.getFullYear()}-${padWithZeros(weekCount, 2)}`;
    case "dekad":
      const dekadCount = dekadInYear(d);
      return `${d.getFullYear()}-${padWithZeros(dekadCount, 2)}`;
    case "month":
      const monthCount = d.getMonth() + 1;
      return `${d.getFullYear()}-${padWithZeros(monthCount, 2)}`;
    case "season":
      const month = d.getMonth() + 1;
      let seasonName = null;
      if (month >= 3 && month <= 5) {
        seasonName = "mam";
      } else if (month >= 6 && month <= 8) {
        seasonName = "jja";
      } else if (month >= 9 && month <= 11) {
        seasonName = "son";
      } else {
        seasonName = "djf";
      }
      return `${d.getFullYear()}-${seasonName}`;
    case "tropical-season":
      let tropicalSeasonName = null;
      if (d.getMonth() + 1 >= 5 && d.getMonth() + 1 <= 10) {
        tropicalSeasonName = "mjjaso";
      } else {
        tropicalSeasonName = "ndjfma";
      }
      return `${d.getFullYear()}-${tropicalSeasonName}`;
    case "year":
      return `${d.getFullYear()}`;
    case "decade":
      return `${d.getFullYear().toString().substring(0, 3)}0`;
    case "decade-ad":
      return `${d.getFullYear().toString().substring(0, 3)}1`;
    default:
      throw new ProcessError({
        name: "UnknownPeriodValue",
        message: `Value '${period}' is not an allowed value for period.`,
      });
  }
};

const generateDatesInRangeByPeriod = (minDate, maxDate, period) => {
  const addPeriodToDate = (currentDate, period) => {
    let newDate = new Date(currentDate);
    switch (period) {
      case "hour":
        newDate.setHours(newDate.getHours() + 1);
        return newDate.toISOString();
      case "day":
        newDate.setDate(newDate.getDate() + 1);
        return newDate.toISOString();
      case "week":
        newDate.setDate(newDate.getDate() + 7);
        return newDate.toISOString();
      case "dekad":
        if (newDate.getDate() > 20) {
          newDate.setDate(1);
          newDate.setMonth(newDate.getMonth() + 1);
        } else {
          newDate.setDate(newDate.getDate() + 10);
        }
        return newDate.toISOString();
      case "month":
        newDate.setMonth(newDate.getMonth() + 1);
        return newDate.toISOString();
      case "season":
        newDate.setMonth(newDate.getMonth() + 3);
        return newDate.toISOString();
      case "tropical-season":
        newDate.setMonth(newDate.getMonth() + 6);
        return newDate.toISOString();
      case "year":
        newDate.setFullYear(newDate.getFullYear() + 1);
        return newDate.toISOString();
      case "decade":
        newDate.setFullYear(newDate.getFullYear() + 10);
        return newDate.toISOString();
      case "decade-ad":
        newDate.setFullYear(newDate.getFullYear() + 10);
        return newDate.toISOString();
      default:
        throw new ProcessError({
          name: "UnknownPeriodValue",
          message: `Value '${period}' is not an allowed value for period.`,
        });
    }
  };

  const dates = [];
  let currentDate = minDate;

  while (currentDate <= maxDate) {
    dates.push(currentDate);
    currentDate = addPeriodToDate(currentDate, period);
  }

  return dates;
};

const getMinMaxDate = (labels) => {
  let minDate = parse_rfc3339(labels[0]).value;
  let maxDate = new Date(minDate).toISOString();

  for (let i = 1; i < labels.length; i++) {
    const currentDate = parse_rfc3339(labels[i]).value;

    if (currentDate < minDate) {
      minDate = currentDate;
    }

    if (currentDate > maxDate) {
      maxDate = currentDate;
    }
  }

  return { minDate, maxDate };
};

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
