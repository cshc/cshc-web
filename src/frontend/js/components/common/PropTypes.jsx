import PropTypes from 'prop-types';

const FilterValuePropType = PropTypes.oneOfType([
  PropTypes.bool,
  PropTypes.string,
  PropTypes.number,
  PropTypes.array,
]);

module.exports = {
  FilterValuePropType,
};
