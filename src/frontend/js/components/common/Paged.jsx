import { UrlQueryParamTypes } from 'react-url-query';

const urlPropsQueryConfig = {
  page: {
    type: UrlQueryParamTypes.number,
  },
  pageSize: {
    type: UrlQueryParamTypes.number,
  },
  sorted: {
      type: UrlQueryParamTypes.json,
    },
};

export default urlPropsQueryConfig;
