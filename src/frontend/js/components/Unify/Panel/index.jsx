import React from 'react';
import PropTypes from 'prop-types';
import classnames from 'classnames';

/**
 * Represents a Unify (Bootstrap) panel
 * 
 * Ref: https://htmlstream.com/preview/unify-v2.2/unify-main/shortcodes/shortcode-base-panels.html
 */
const Panel = ({ className, outlineColor, headerColor, icon, title, children }) => {
  const cardClass = classnames('card rounded-0', className, {
    [`card-outline-${outlineColor}`]: outlineColor,
  });
  const headerClass = classnames('g-font-size-16 card-header h5 rounded-0', {
    'text-white g-brd-transparent': headerColor,
    [`g-bg-${headerColor}`]: headerColor,
  });
  const iconClass = classnames('g-mr-10', {
    [icon]: icon,
  });
  return (
    <div className={cardClass}>
      <h3 className={headerClass}>
        {icon && <i className={iconClass} />}
        {title}
      </h3>

      {children}
    </div>
  );
};

Panel.propTypes = {
  className: PropTypes.string,
  outlineColor: PropTypes.string,
  headerColor: PropTypes.string,
  icon: PropTypes.string,
  title: PropTypes.node,
  children: PropTypes.node,
};

Panel.defaultProps = {
  className: 'g-mb-20',
  outlineColor: undefined,
  headerColor: undefined,
  icon: undefined,
  title: '',
  children: undefined,
};

export default Panel;
