import React from 'react';
import PropTypes from 'prop-types';

/**
 * React implementation of a Unify/Bootstrap progress bar.
 * 
 * Ref: https://htmlstream.com/preview/unify-v2.2/unify-main/shortcodes/shortcode-base-progress-bars.html#shortcode16
 */
const ProgressBar = ({ label, value, progressItems, min, max }) => (
  <div className="g-mb-10">
    <h6>
      {label}
      <span className="float-right g-ml-10">{value}</span>
    </h6>

    <div className="progress g-height-20 rounded-0">
      {progressItems.map(item => (
        <div
          key={item.color}
          className="progress-bar u-progress-bar--sm"
          role="progressbar"
          style={{ width: `${100 * (item.value / max)}%`, backgroundColor: item.color }}
          aria-valuenow={item.value}
          aria-valuemin={min}
          aria-valuemax={max}
        />
      ))}
    </div>
  </div>
);

ProgressBar.propTypes = {
  label: PropTypes.string.isRequired,
  value: PropTypes.number.isRequired,
  progressItems: PropTypes.arrayOf(
    PropTypes.shape({
      value: PropTypes.number.isRequired,
      color: PropTypes.string.isRequired,
    }).isRequired,
  ).isRequired,
  min: PropTypes.number,
  max: PropTypes.number,
};

ProgressBar.defaultProps = {
  min: 0,
  max: 100,
};

export default ProgressBar;
