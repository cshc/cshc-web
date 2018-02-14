import PropTypes from 'prop-types';

const SlidePropType = PropTypes.shape({
  label: PropTypes.string.isRequired,
  // navigationNode should be a Redux connect function, providing
  // label, icon and complete props to a NavigationNode component.
  navigationNode: PropTypes.func.isRequired,
  // If not provided, the string label prop will be used as a slide title isntead.
  title: PropTypes.node,
});

const SlideListPropType = PropTypes.arrayOf(SlidePropType);

module.exports = {
  SlidePropType,
  SlideListPropType,
};
