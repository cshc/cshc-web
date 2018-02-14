import React from 'react';
import PropTypes from 'prop-types';
import classnames from 'classnames';
import styles from './style.scss';

/** 
 * A single navigation node for the multi-step form.
 * 
 * Contains an icon and label. Icon backgound is different
 * if the 'current' prop is true, and displays a check icon
 * if the 'complete' prop is true (and its not current).
 */
const NavigationNode = ({ label, icon, complete, current, onClick }) => {
  const nodeClass = classnames(styles.msNode, {
    [styles.complete]: complete && !current,
    [styles.current]: current,
  });
  const iconClass = classnames({
    [icon]: current || !complete,
    'fa fa-check': !current && complete,
  });
  return (
    <div className={nodeClass} onClick={onClick} role="link" tabIndex="0">
      <i className={styles.msIconBar}>
        <span className={styles.msIconLink}>
          <div className={styles.msIconBox}>
            <i className={iconClass} />
          </div>
        </span>
      </i>
      <span className={styles.msNodeLabel}>{label}</span>
    </div>
  );
};

NavigationNode.propTypes = {
  label: PropTypes.string.isRequired,
  icon: PropTypes.string.isRequired,
  current: PropTypes.bool.isRequired,
  onClick: PropTypes.func.isRequired,
  complete: PropTypes.bool,
};

NavigationNode.defaultProps = {
  complete: false,
};

export default NavigationNode;
