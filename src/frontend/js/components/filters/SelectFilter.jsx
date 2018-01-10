import React from 'react';
import PropTypes from 'prop-types';
import classnames from 'classnames';
import Select from 'react-select';
import { FilterValuePropType } from 'components/common/PropTypes';
import styles from './style.scss';

const SelectFilter = ({
  label,
  options,
  filterName,
  filterValue,
  onSetFilter,
  openUpwards,
  inline,
  stacked,
  ...props
}) => {
  const wrapperStyle = classnames(styles.filter, styles.select, 'g-py-10', {
    [styles.upwards]: openUpwards,
    [styles.inline]: inline,
    [styles.stacked]: stacked,
  });
  const controlStyle = classnames(styles.filterControl, {
    [styles.stackedControl]: stacked,
  });
  const onChange = (value) => {
    onSetFilter(filterName, value);
  };
  return (
    <div className={wrapperStyle}>
      {label && <div className={styles.filterLabel}>{label}</div>}
      <div className={controlStyle}>
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
  stacked: PropTypes.bool,
};

SelectFilter.defaultProps = {
  filterValue: undefined,
  openUpwards: false,
  label: undefined,
  inline: false,
  stacked: false,
};

export default SelectFilter;
