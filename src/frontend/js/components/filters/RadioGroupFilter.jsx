import React from 'react';
import PropTypes from 'prop-types';
import RadioGroup from 'components/common/RadioGroup';

const RadioGroupFilter = ({ options, filterName, filterValue, onSetFilter }) => {
  const onChange = (value) => {
    onSetFilter(filterName, value);
  };
  return (
    <RadioGroup
      className="g-py-10"
      options={options}
      name={filterName}
      selectedValue={filterValue}
      onChange={onChange}
    />
  );
};

const valueType = PropTypes.oneOfType([PropTypes.bool, PropTypes.string, PropTypes.number]);

RadioGroupFilter.propTypes = {
  filterName: PropTypes.string.isRequired,
  onSetFilter: PropTypes.func.isRequired,
  filterValue: valueType,
  options: PropTypes.arrayOf(
    PropTypes.shape({
      label: PropTypes.string,
      value: PropTypes.oneOfType([PropTypes.string, PropTypes.number]),
    }),
  ).isRequired,
};

RadioGroupFilter.defaultProps = {
  filterValue: undefined,
};

export default RadioGroupFilter;
