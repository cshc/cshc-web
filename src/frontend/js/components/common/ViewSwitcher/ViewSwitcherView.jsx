import React from 'react';
import PropTypes from 'prop-types';

const ViewSwitcherView = ({ currentView, onSelect, iconClass, label }) => {
  const className =
    label === currentView ? 'btn g-mr-10 u-btn-primary' : 'btn g-mr-10 u-btn-outline-primary';
  return (
    <a role="button" tabIndex={0} className={className} onClick={() => onSelect(label)}>
      <i className={`${iconClass} g-mr-5`} />
      {label}
    </a>
  );
};

// Note: currentView and onSelect props will be automatically passed to ViewSwitcherView by the
// parent ViewSwitcher component.
ViewSwitcherView.propTypes = {
  currentView: PropTypes.string,
  onSelect: PropTypes.func,
  iconClass: PropTypes.string.isRequired,
  label: PropTypes.string.isRequired,
};

ViewSwitcherView.defaultProps = {
  currentView: undefined,
  onSelect: () => {},
};

export default ViewSwitcherView;
