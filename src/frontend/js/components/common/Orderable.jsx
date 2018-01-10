import { addUrlProps, UrlQueryParamTypes } from 'react-url-query';

const urlPropsQueryConfig = {
  orderBy: {
    type: UrlQueryParamTypes.string,
  },
};

export default addUrlProps({ urlPropsQueryConfig });
