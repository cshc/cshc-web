import React from 'react';
import PropTypes from 'prop-types';
import classnames from 'classnames';
import Timeline2Item from './Timeline2Item';
import TimelineBigItem from './TimelineBigItem';

/**
 *  Represents a timeline. 
 * 
 *  Ref: https://htmlstream.com/preview/unify-v2.2/unify-main/shortcodes/shortcode-blocks-timelines.html
 *       https://htmlstream.com/preview/unify-v2.2/unify-main/pages/page-profile-profile-1.html
 */
const Timeline2 = ({ className, children }) => (
  <ul className={classnames(className, 'row list-unstyled')}>{children}</ul>
);

Timeline2.propTypes = {
  className: PropTypes.string,
  children: PropTypes.arrayOf(PropTypes.oneOfType([TimelineBigItem, Timeline2Item])).isRequired,
};

Timeline2.defaultProps = {
  className: undefined,
};

export default Timeline2;
