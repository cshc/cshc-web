import React from 'react';
import PropTypes from 'prop-types';
import styles from './style.scss';

/**
 * Switches between various view states. 
 */
const ViewSwitcher = ({ currentView, className, onSelectViewType, label, children }) => {
  const childrenWithProps = React.Children.map(children, child =>
    React.cloneElement(child, {
      currentView,
      onSelect: onSelectViewType,
    }),
  );
  return (
    <div className={`${styles.viewTypes} ${className}`}>
      <span className="g-mr-10">{label}</span>
      {childrenWithProps}
    </div>
  );
};

ViewSwitcher.propTypes = {
  currentView: PropTypes.string.isRequired,
  onSelectViewType: PropTypes.func.isRequired,
  className: PropTypes.string,
  label: PropTypes.string,
  children: PropTypes.node.isRequired,
};

ViewSwitcher.defaultProps = {
  className: 'g-mb-15',
  label: 'Display:',
};

export default ViewSwitcher;
