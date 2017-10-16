import React from 'react';
import PropTypes from 'prop-types';

const ProgressBar = ({ label, value, progressValue, min, max, color }) => (
  <div className="g-mb-10">
    <h6>
      {label}
      <span className="float-right g-ml-10">{value}</span>
    </h6>

    <div className="progress g-height-20 rounded-0">
      <div
        className={`progress-bar u-progress-bar--sm g-bg-${color}`}
        role="progressbar"
        style={{ width: `${progressValue}%` }}
        aria-valuenow={progressValue}
        aria-valuemin={min}
        aria-valuemax={max}
      />
    </div>
  </div>
);

ProgressBar.propTypes = {
  label: PropTypes.string.isRequired,
  value: PropTypes.number.isRequired,
  progressValue: PropTypes.number.isRequired,
  min: PropTypes.number,
  max: PropTypes.number,
  color: PropTypes.string,
};

ProgressBar.defaultProps = {
  min: 0,
  max: 100,
  color: 'teal',
};

export default ProgressBar;
