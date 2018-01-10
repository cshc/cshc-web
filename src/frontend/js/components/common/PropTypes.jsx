import PropTypes from 'prop-types';
import { DefaultPageSize } from 'util/constants';

const FilterValuePropType = PropTypes.oneOfType([
  PropTypes.bool,
  PropTypes.string,
  PropTypes.number,
  PropTypes.array,
]);

const PageQueryPropType = PropTypes.shape({
  pageIndex: PropTypes.number,
  first: PropTypes.number,
  after: PropTypes.string,
  before: PropTypes.string,
});

const DefaultPageQueryProps = {
  pageIndex: 0,
  first: DefaultPageSize,
  after: undefined,
  before: undefined,
};

module.exports = {
  FilterValuePropType,
  PageQueryPropType,
  DefaultPageQueryProps,
};
