import { default as dateFormat } from 'date-fns/format';
import addDays from 'date-fns/add_days';
import compareDesc from 'date-fns/compare_desc';
import isSaturday from 'date-fns/is_saturday';

const toTitleCase = str =>
  str.replace(/\w\S*/g, txt => txt.charAt(0).toUpperCase() + txt.substr(1).toLowerCase());

const toGraphQLId = (nodeType, id) => btoa(`${nodeType}:${id}`);

const toModelId = graphQLId => atob(graphQLId).split(':')[1];

const getPosition = (position) => {
  if (!position) return undefined;
  const pos = position.split(',');
  return {
    lat: parseFloat(pos[0]),
    lng: parseFloat(pos[1]),
  };
};

const nonZero = value => (value > 0 ? value : null);

const rounded = (value, precision = 1) => (value ? value.toFixed(precision) : null);

const djangoDate = (date, separator = '-') => {
  const parts = date.split(separator);
  return dateFormat(
    new Date(parseInt(parts[2], 10), parseInt(parts[1], 10) - 1, parseInt(parts[0], 10)),
    'YYYY-MM-DD',
  );
};

const saturdaysBetweenDates = (date1, date2) => {
  if (!date1 || !date2) return null;
  let d = addDays(date1, 1);
  const saturdays = [];
  while (compareDesc(d, date2) > 0) {
    if (isSaturday(d)) {
      saturdays.push(d);
    }
    d = addDays(d, 1);
  }
  return saturdays;
};

module.exports = {
  toTitleCase,
  toGraphQLId,
  toModelId,
  getPosition,
  nonZero,
  rounded,
  djangoDate,
  saturdaysBetweenDates,
};
