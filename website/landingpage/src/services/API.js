import axios from 'axios';

const API_BASE_URL = `https://${process.env.REACT_APP_DOMAIN_SUFFIX}.bowtiedlist.com/`;

const client = axios.create({
  baseURL: API_BASE_URL,
  timeout: 900000, // Adjust timeout as needed
  headers: {
    'Content-Type': 'application/json;charset=utf-8'
  }
});

const API = {
  get(url, conf = {}) {
    return client.get(url, conf)
      .then(response => response.data)
      .catch(error => Promise.reject(error.response.data));
  },

  delete(url, conf = {}) {
    return client.delete(url, conf)
      .then(response => response.data)
      .catch(error => Promise.reject(error.response.data));
  },

  head(url, conf = {}) {
    return client.head(url, conf)
      .then(response => response.data)
      .catch(error => Promise.reject(error.response.data));
  },

  options(url, conf = {}) {
    return client.options(url, conf)
      .then(response => response.data)
      .catch(error => Promise.reject(error.response.data));
  },

  post(url, data = {}, conf = {}) {
    return client.post(url, data, conf)
      .then(response => response.data)
      .catch(error => Promise.reject(error.response.data));
  },

  put(url, data = {}, conf = {}) {
    return client.put(url, data, conf)
      .then(response => response.data)
      .catch(error => Promise.reject(error.response.data));
  },

  patch(url, data = {}, conf = {}) {
    return client.patch(url, data, conf)
      .then(response => response.data)
      .catch(error => Promise.reject(error.response.data));
  },
};

export default API;
