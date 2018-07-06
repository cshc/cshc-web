import React from 'react';
import { addUrlProps } from 'react-url-query';
import Paged from 'components/common/Paged';
import BooleanFilter from './BooleanFilter';
import SelectFilter from './SelectFilter';
import OptionListFilter from './OptionListFilter';
import TextFilter from './TextFilter';
import DateFilter from './DateFilter';

// const handlerName = urlQueryPropName =>
//   `onChange${urlQueryPropName.charAt(0).toUpperCase() + urlQueryPropName.substr(1)}`;

const UrlFilter = WrappedFilter => ({
  filterName,
  defaultValue,
  urlQueryConfig,
  ...otherProps
}) => {
  const urlPropsQueryConfig = {
    [filterName]: urlQueryConfig,
  };

  const UrlQueryFilter = props => (
    <WrappedFilter
      filterName={props.filterName}
      filterValue={
        props[props.filterName] === undefined ? props.defaultValue : props[props.filterName]
      }
      onSetFilter={(_, filterValue) => {
        const newValue = filterValue === props.defaultValue ? undefined : filterValue;
        // We need to reset the page number to 1 every time we re-filter
        props.onChangeUrlQueryParams({
          page: 1,
          [props.filterName]: newValue,
        });
      }}
      {...otherProps}
    />
  );

  const UrlWrapped = addUrlProps({
    urlPropsQueryConfig: {
      ...urlPropsQueryConfig,
      ...Paged,
    },
  })(UrlQueryFilter);

  return (
    <UrlWrapped
      {...otherProps}
      filterName={filterName}
      defaultValue={defaultValue}
      urlQueryConfig={urlQueryConfig}
    />
  );
};

module.exports = {
  BooleanFilter: UrlFilter(BooleanFilter),
  SelectFilter: UrlFilter(SelectFilter),
  OptionListFilter: UrlFilter(OptionListFilter),
  TextFilter: UrlFilter(TextFilter),
  DateFilter: UrlFilter(DateFilter),
};
