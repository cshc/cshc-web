import React from 'react';
import PropTypes from 'prop-types';
import classnames from 'classnames';
import Select from 'react-select';
import styles from './style.scss';

const SelectFilter = ({ options, filterName, filterValue, onSetFilter, openUpwards, ...props }) => {
  const wrapperStyle = classnames(styles.select, 'g-py-10', {
    [styles.upwards]: openUpwards,
  });
  const onChange = (value) => {
    onSetFilter(filterName, value);
  };
  return (
    <div className={wrapperStyle}>
      <Select
        options={options}
        simpleValue
        clearable
        searchable
        name={filterName}
        value={filterValue}
        onChange={onChange}
        {...props}
      />
    </div>
  );
};

const valueType = PropTypes.oneOfType([PropTypes.bool, PropTypes.string, PropTypes.number]);

SelectFilter.propTypes = {
  filterName: PropTypes.string.isRequired,
  onSetFilter: PropTypes.func.isRequired,
  filterValue: valueType,
  options: PropTypes.arrayOf(
    PropTypes.shape({
      label: PropTypes.string,
      value: PropTypes.oneOfType([PropTypes.string, PropTypes.number]),
    }),
  ).isRequired,
  openUpwards: PropTypes.bool,
};

SelectFilter.defaultProps = {
  filterValue: undefined,
  openUpwards: false,
};

export default SelectFilter;
