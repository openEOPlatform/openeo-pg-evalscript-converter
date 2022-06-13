const DATE_TIME_TYPES = {
  date: "date",
  date_time: "date-time",
  milliseconds_of_day: "milliseconds-of-day",
}

function parse_rfc3339(dateTime, default_h = 0, default_m = 0, default_s = 0) {
  const regexDateTime =
    "^([0-9]{4})-([0-9]{2})-([0-9]{2})([Tt]([0-9]{2}):([0-9]{2}):([0-9]{2})(\.[0-9]+)?)([Zz]|([+-])([0-9]{2}):([0-9]{2}))";
  const regexDate = "^([0-9]{4})-([0-9]{2})-([0-9]{2})$";

  try {
    const matchDateTime = dateTime.match(regexDateTime);
    const matchDate = dateTime.match(regexDate);

    if (matchDateTime || matchDate) {
      return {
        type: matchDate ? DATE_TIME_TYPES.date : DATE_TIME_TYPES.date_time,
        value: new Date(dateTime).toISOString(),
      };
    }
  } catch (err) {}

  return null;
}

function extract_milliseconds_of_day(dateTime) {
  const regexTime = "(([0-9]{2}):([0-9]{2}):([0-9]{2})(\.[0-9]+)?)([Zz]|([+-])([0-9]{2}):([0-9]{2}))";

  try {
    const matchTime = dateTime.match(regexTime);

    if (matchTime) {
      return {
        type: DATE_TIME_TYPES.milliseconds_of_day,
        value: new Date('1970-01-01T' + matchTime[0]).getTime(),
      };
    }
  } catch (err) {}

  return null;
}

const formatLabelByPeriod = (period, label) => {
  const dayInYear = (date) => {
    return (
      (Date.UTC(date.getUTCFullYear(), date.getUTCMonth(), date.getUTCDate()) -
        Date.UTC(date.getUTCFullYear(), 0, 0)) /
      24 /
      60 /
      60 /
      1000
    );
  };

  const dekadInYear = (date) => {
    const monthCount = date.getUTCMonth();
    const dekadCount = Math.floor((date.getUTCDate() - 1) / 10) + 1;
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
      const days = d.getUTCDate();
      const months = d.getUTCMonth() + 1;
      return `${d.getUTCFullYear()}-${padWithZeros(months, 2)}-${padWithZeros(
        days,
        2
      )}-${hourCount}`;
    case "day":
      const dayCount = dayInYear(d);
      return `${d.getUTCFullYear()}-${padWithZeros(dayCount, 3)}`;
    case "week":
      const weekCount = Math.ceil(dayInYear(d) / 7);
      return `${d.getUTCFullYear()}-${padWithZeros(weekCount, 2)}`;
    case "dekad":
      const dekadCount = dekadInYear(d);
      return `${d.getUTCFullYear()}-${padWithZeros(dekadCount, 2)}`;
    case "month":
      const monthCount = d.getUTCMonth() + 1;
      return `${d.getUTCFullYear()}-${padWithZeros(monthCount, 2)}`;
    case "season":
      const month = d.getUTCMonth() + 1;
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
      return `${d.getUTCFullYear()}-${seasonName}`;
    case "tropical-season":
      let tropicalSeasonName = null;
      if (d.getUTCMonth() + 1 >= 5 && d.getUTCMonth() + 1 <= 10) {
        tropicalSeasonName = "mjjaso";
      } else {
        tropicalSeasonName = "ndjfma";
      }
      return `${d.getUTCFullYear()}-${tropicalSeasonName}`;
    case "year":
      return `${d.getUTCFullYear()}`;
    case "decade":
      return `${d.getUTCFullYear().toString().substring(0, 3)}0`;
    case "decade-ad":
      return `${d.getUTCFullYear().toString().substring(0, 3)}1`;
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
        newDate.setUTCHours(newDate.getUTCHours() + 1);
        return newDate.toISOString();
      case "day":
        newDate.setUTCDate(newDate.getUTCDate() + 1);
        return newDate.toISOString();
      case "week":
        newDate.setUTCDate(newDate.getUTCDate() + 7);
        return newDate.toISOString();
      case "dekad":
        if (newDate.getUTCDate() > 20) {
          newDate.setUTCDate(1);
          newDate.setUTCMonth(newDate.getUTCMonth() + 1);
        } else {
          newDate.setUTCDate(newDate.getUTCDate() + 10);
        }
        return newDate.toISOString();
      case "month":
        newDate.setUTCMonth(newDate.getUTCMonth() + 1);
        return newDate.toISOString();
      case "season":
        newDate.setUTCMonth(newDate.getUTCMonth() + 3);
        return newDate.toISOString();
      case "tropical-season":
        newDate.setUTCMonth(newDate.getUTCMonth() + 6);
        return newDate.toISOString();
      case "year":
        newDate.setUTCFullYear(newDate.getUTCFullYear() + 1);
        return newDate.toISOString();
      case "decade":
        newDate.setUTCFullYear(newDate.getUTCFullYear() + 10);
        return newDate.toISOString();
      case "decade-ad":
        newDate.setUTCFullYear(newDate.getUTCFullYear() + 10);
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
  let maxDate = minDate;

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
