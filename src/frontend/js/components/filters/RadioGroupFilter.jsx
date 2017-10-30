import React from 'react';
import PropTypes from 'prop-types';
import classnames from 'classnames';
import RadioGroup from 'components/common/RadioGroup';
import styles from './style.scss';

const RadioGroupFilter = ({ options, filterName, filterValue, onSetFilter }) => {
  const wrapperClass = classnames('g-py-10');
  const onChange = (value) => {
    onSetFilter(filterName, value);
  };
  return (
    <RadioGroup
      className={wrapperClass}
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
