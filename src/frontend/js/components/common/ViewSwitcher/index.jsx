import React from 'react';
import PropTypes from 'prop-types';
import styles from './style.scss';

/**
 * Switches between various view states. 
 * 
 * Each view must define an iconClass, a label and an onSelect callback function.
 */
const ViewSwitcher = ({ className, label, currentView, views }) => {
  views.forEach((view) => {
    view.className =
      view.label === currentView
        ? 'btn g-mr-10 u-btn-primary'
        : 'btn g-mr-10 u-btn-outline-primary';
  });
  return (
    <div className={`${styles.viewTypes} ${className}`}>
      <span className="g-mr-10">{label}</span>
      {views.map(view => (
        <a
          key={view.label}
          role="button"
          tabIndex={0}
          className={view.className}
          onClick={view.onSelect}
        >
          <i className={`${view.iconClass} g-mr-5`} />
          {view.label}
        </a>
      ))}
    </div>
  );
};

ViewSwitcher.propTypes = {
  className: PropTypes.string,
  label: PropTypes.string,
  currentView: PropTypes.string.isRequired,
  views: PropTypes.arrayOf(
    PropTypes.shape({
      iconClass: PropTypes.string,
      label: PropTypes.string,
      onSelect: PropTypes.func,
    }),
  ).isRequired,
};

ViewSwitcher.defaultProps = {
  className: 'g-mb-15',
  label: 'Display:',
};

export default ViewSwitcher;
