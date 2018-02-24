import PropTypes from 'prop-types';

const MemberPropType = PropTypes.shape({
  id: PropTypes.number.isRequired,
  firstName: PropTypes.string.isRequired,
  lastName: PropTypes.string.isRequired,
  profilePicUrl: PropTypes.string,
  prefPosition: PropTypes.string,
  isUmpire: PropTypes.bool,
  squad: PropTypes.shape({
    slug: PropTypes.string,
    name: PropTypes.string,
  }),
});

module.exports = {
  MemberPropType,
};
