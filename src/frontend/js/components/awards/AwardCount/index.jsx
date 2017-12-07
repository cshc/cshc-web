import React from 'react';
import PropTypes from 'prop-types';
import styles from './style.scss';

const AwardCount = ({ iconClass, awardCount }) => {
  const wrapperClass = awardCount === 0 ? styles.hide : styles.wrapper;
  return (
    <div className={wrapperClass}>
      <i className={`fa fa-3x fa-${iconClass}`} />
      {awardCount > 0 && <div className={styles.awardCount}>{awardCount}</div>}
    </div>
  );
};

AwardCount.propTypes = {
  iconClass: PropTypes.oneOf(['star-o', 'lemon-o']).isRequired,
  awardCount: PropTypes.number.isRequired,
};

export default AwardCount;
