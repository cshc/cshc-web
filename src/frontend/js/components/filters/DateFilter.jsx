import React from 'react';
import PropTypes from 'prop-types';
import classnames from 'classnames';
import { DateInput } from 'components/Unify';
import { FilterValuePropType } from 'components/common/PropTypes';
import styles from './style.scss';

const DateFilter = ({
  label,
  filterName,
  filterValue,
  onSetFilter,
  openUpwards,
  inline,
  stacked,
}) => {
  const wrapperStyle = classnames(styles.filter, styles.select, 'g-py-10', {
    [styles.upwards]: openUpwards,
    [styles.inline]: inline,
    [styles.stacked]: stacked,
  });
  const controlStyle = classnames(styles.filterLabel, {
    [styles.stackedControl]: stacked,
  });
  const onChange = (value) => {
    onSetFilter(filterName, value);
  };
  return (
    <div className={wrapperStyle}>
      {label && <div className={styles.filterLabel}>{label}</div>}
      <div className={controlStyle}>
        <DateInput name={filterName} value={filterValue} onChange={onChange} />
      </div>
    </div>
  );
};

DateFilter.propTypes = {
  label: PropTypes.string,
  filterName: PropTypes.string.isRequired,
  onSetFilter: PropTypes.func.isRequired,
  filterValue: FilterValuePropType,
  openUpwards: PropTypes.bool,
  inline: PropTypes.bool,
  stacked: PropTypes.bool,
};

DateFilter.defaultProps = {
  filterValue: undefined,
  openUpwards: false,
  label: undefined,
  inline: false,
  stacked: false,
};

export default DateFilter;
