import axios from 'axios';
import { Auth } from 'aws-amplify';


const getClient = async (clientIdOverride, useCache) => {

  // const clientID = clientIdOverride || sessionStorage.getItem('selectedClient');
  const JWT =  await Auth.currentSession().then(data => data.getIdToken().getJwtToken());
  const identityToken = await Auth.currentCredentials();
  const cache = await caches.open(`bowtiedlist`);

  const options = {
    baseURL: `https://${process.env.REACT_APP_DOMAIN_SUFFIX}.bowtiedlist.com/`,
    timeout: 900000,
    headers: {
      // 'Accept-Encoding':'gzip, deflate, br', //doesn't seem to be necessary? also chrome yells at me for trying to do it
      'Content-Type': 'application/json;charset=utf-8',
      // 'client-id': clientID,
      "Authorization": JWT,
      "key": identityToken.accessKeyId,
      "secret": identityToken.secretAccessKey,
      "session": identityToken.sessionToken
    }
  };

  const client = axios.create(options);

  if (useCache) {

    const requestHandler = async (request) => {
      if (request.method === 'GET' || 'get') {
        const response = await cache.match(request.baseURL + request.url)
        if (response) {
          request.headers.cached = true;
          request.data = await response.json();
          return Promise.reject(request);
        } else {
          return request;
        }
      } else {
        return request;
      }
    };
  
    // Add a request interceptor
    client.interceptors.request.use(
      requestConfig => requestHandler(requestConfig),
      (requestError) => {
        // this is where we could universally log request errors
        console.log('Request error: ', requestError);
        return Promise.reject(requestError);
      },
    );
  
    // Add a response interceptor
    client.interceptors.response.use(
      (response) => {
        if ((response.config?.method === 'GET' || 'get') && [200,201,202,203,204,205].includes(response.status)) {
          const now = Date.now();
          response.headers.timeCached = new Date(now).toLocaleString();
          cache.put(response.config.baseURL + response.config.url, new Response(JSON.stringify(response.data), response));
        }
        return response;
      },
      (error) => {
        if (error.headers?.cached === true) {
          return Promise.resolve(error);
        }
        return Promise.reject(error);
      }
    );
  
    return client;

  } else { //below is what we do for all requests where we don't explicitly say useCache

    // Add a request interceptor
    client.interceptors.request.use(
      requestConfig => requestConfig,
      (requestError) => {
        // this is where we could universally log request errors
        console.log('Request error: ', requestError);

        return Promise.reject(requestError);
      },
    );

    // Add a response interceptor
    client.interceptors.response.use(
      async (response) => {
        const isCached = await cache.match(response.request?.responseURL);
        if (!!isCached && (response.config?.method === 'GET' || 'get') && [200,201,202,203,204,205].includes(response.status)) {
          const now = Date.now();
          response.headers.timeCached = new Date(now).toLocaleString();
          cache.put(response.config.baseURL + response.config.url, new Response(JSON.stringify(response.data), response));
        }
        return response;
      },
      (error) => {
        if (error?.response?.status >= 400) {
          // this is where we could universally log response errors
          console.log('Response error: ', error);
          console.log('response when error: ', error?.response?.data?.body);
        }

        return Promise.reject(error.response?.data);
      },
    );

    return client;
  }
};


const API = {
  async get(url, { conf = {}, clientId = null, useCache = false } = {}) {
    const cli = await getClient(clientId, useCache);
    return cli.get(url, conf)
      .then(response => Promise.resolve(response))
      .catch(error => Promise.reject(error));
  },

  async delete(url, { conf = {}, clientId = null, useCache = false } = {}) {
    const cli = await getClient(clientId, useCache);
    return cli.delete(url, conf)
      .then(response => Promise.resolve(response))
      .catch(error => Promise.reject(error));
  },

  async head(url, { conf = {}, clientId = null, useCache = false } = {}) {
    const cli = await getClient(clientId, useCache);
    return cli.head(url, conf)
      .then(response => Promise.resolve(response))
      .catch(error => Promise.reject(error));
  },

  async options(url, { conf = {}, clientId = null, useCache = false } = {}) {
    const cli = await getClient(clientId, useCache);
    return cli.options(url, conf)
      .then(response => Promise.resolve(response))
      .catch(error => Promise.reject(error));
  },

  async post(url, { data = {}, conf = {}, clientId = null, useCache = false } = {}) {
    const cli = await getClient(clientId, useCache);
    return cli.post(url, data, conf)
      .then(response => Promise.resolve(response))
      .catch(error => Promise.reject(error));
  },

  async put(url, { data = {}, conf = {}, clientId = null, useCache = false } = {}) {
    const cli = await getClient(clientId, useCache);
    return cli.put(url, data, conf)
      .then(response => Promise.resolve(response))
      .catch(error => Promise.reject(error));
  },

  async patch(url, { data = {}, conf = {}, clientId = null, useCache = false } = {}) {
    const cli = await getClient(clientId, useCache);
    return cli.patch(url, data, conf)
      .then(response => Promise.resolve(response))
      .catch(error => Promise.reject(error));
  },
};

export default API;