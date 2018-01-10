import { addUrlProps, UrlQueryParamTypes } from 'react-url-query';

const urlPropsQueryConfig = {
  page: {
    type: UrlQueryParamTypes.number,
  },
  pageSize: {
    type: UrlQueryParamTypes.number,
  },
};

export default addUrlProps({ urlPropsQueryConfig });
