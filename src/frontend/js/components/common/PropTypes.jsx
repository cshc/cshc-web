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

const SelectValueLabelOptionPropType = PropTypes.shape({
  value: PropTypes.oneOfType([PropTypes.string, PropTypes.number]).isRequired,
  label: PropTypes.string.isRequired,
});

const SelectValueLabelOptionsPropType = PropTypes.arrayOf(SelectValueLabelOptionPropType);

const SelectOptionPropTypes = PropTypes.oneOfType([
  PropTypes.string,
  SelectValueLabelOptionsPropType,
]);

const SelectOptionsPropTypes = PropTypes.arrayOf(SelectOptionPropTypes);

module.exports = {
  FilterValuePropType,
  PageQueryPropType,
  DefaultPageQueryProps,
  SelectValueLabelOptionPropType,
  SelectValueLabelOptionsPropType,
  SelectOptionsPropTypes,
};
