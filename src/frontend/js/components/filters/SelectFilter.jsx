import React from 'react';
import PropTypes from 'prop-types';
import classnames from 'classnames';
import Select from 'react-select';
import { FilterValuePropType } from 'components/common/PropTypes';
import filtered from './filterContainer';
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

SelectFilter.propTypes = {
  filterName: PropTypes.string.isRequired,
  onSetFilter: PropTypes.func.isRequired,
  filterValue: FilterValuePropType,
  options: PropTypes.arrayOf(
    PropTypes.shape({
      label: PropTypes.string,
      value: FilterValuePropType,
    }),
  ).isRequired,
  openUpwards: PropTypes.bool,
};

SelectFilter.defaultProps = {
  filterValue: undefined,
  openUpwards: false,
};

export default filtered(SelectFilter);
