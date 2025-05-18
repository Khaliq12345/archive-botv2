export default defineEventHandler(async (event) => {
  const config = useRuntimeConfig();
  const urlAPI = config.public.urlAPI;
  const apiKey = config.public.ApiKey;

  const query = getQuery(event);
  const headers = {
    'accept': 'application/json',
    'x-api-key': apiKey,
    'Content-Type': 'application/json'
  }
  const body = await readBody(event)

  const params = {
    base_url: query.base_url
  }

  console.log(body, urlAPI, params)

  try {
    const response = await $fetch(event.path, {
        baseURL: urlAPI,
        method: 'POST',
        params: params,
        body: body,
        headers: headers as HeadersInit,
    });
    return response
  } catch (err) {
    console.error('Error:', err);
    return null;
  }
})