import type {APIError} from "@/types/ApiTypes"

type HTTPMethod =
  | 'GET'
  | 'POST'

type RequestOptions = {
  method: HTTPMethod,
  headers?: HeadersInit,
  body?: BodyInit
}

function isApiError(error: unknown): error is APIError {
  return (error as APIError).detail !== undefined
}

async function request<T>(url: string, options: RequestOptions): Promise<T> {
  try {
    const response = await fetch(url, options)

    if (!response.ok) {
      const res = await response.json() as APIError
      res.statusText = `${response.status} | ${response.statusText}`
      throw res
    }

    const res = await response.json() as T
    return res
  }

  // Catch, catches only the network related failures. It is Not executed when http response has been arrived.
    catch (error) {
      console.log(error)
      if (isApiError(error)) {
	throw error
      }

      const internalError: APIError = { detail: "Internal Error", statusText: "Internal Error" }

      throw internalError
    }

}

type ApiClientOptions = {
  baseUrl: string;
};

export function createApiClient(apiOptions: ApiClientOptions) {
  return {
    get<T>(url: string, headers?: HeadersInit) {
      return request<T>(apiOptions.baseUrl + url, {
        method: "GET",
        headers,
      });
    },

    post<T>(url: string, body: BodyInit, headers?: HeadersInit) {
      return request<T>(apiOptions.baseUrl + url, {
        method: "POST",
        headers: {
	  "Content-Type": "application/json",
	  ...headers
	},
        body: body,
      });
    },
  };
}
