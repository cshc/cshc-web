import React from 'react';
import PropTypes from 'prop-types';
import classnames from 'classnames';
import Select from 'react-select';
import { FilterValuePropType } from 'components/common/PropTypes';
import filtered from './filterContainer';
import styles from './style.scss';

const SelectFilter = ({
  label,
  options,
  filterName,
  filterValue,
  onSetFilter,
  openUpwards,
  inline,
  ...props
}) => {
  const wrapperStyle = classnames(styles.filter, styles.select, 'g-py-10', {
    [styles.upwards]: openUpwards,
    [styles.inline]: inline,
  });
  const onChange = (value) => {
    onSetFilter(filterName, value);
  };
  return (
    <div className={wrapperStyle}>
      {label && <div className={styles.filterLabel}>{label}</div>}
      <div className={styles.filterControl}>
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
    </div>
  );
};

SelectFilter.propTypes = {
  label: PropTypes.string,
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
  inline: PropTypes.bool,
};

SelectFilter.defaultProps = {
  filterValue: undefined,
  openUpwards: false,
  label: undefined,
  inline: false,
};

export default SelectFilter;
