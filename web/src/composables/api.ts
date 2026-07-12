import { createApiClient } from "@/apiClient/client"
import type { APIBranding, APICapabilities, APIPastedResponse, APIToken, PostPastedPayload } from "@/types/ApiTypes"


// useAPI is a composable that knows how to interact with the pastore api.
export function useAPI() {
	const api_client = createApiClient({ baseUrl: "/api" })

	function getToken(payload: URLSearchParams): Promise<APIToken> {

	  const response = api_client.post<APIToken>("/token", payload, {
	    "Content-Type": "application/x-www-form-urlencoded"
	  })

	  return response

	}

	function getApiCapabilities(): Promise<APICapabilities> {
		const url = "/management/what-is-available"


		const response = api_client.get<APICapabilities>(url)

		return response

	}


	function getBranding(): Promise<APIBranding> {
		const url = "/management/branding"

		const response = api_client.get<APIBranding>(url)

		return response

	}


	async function postPasted(payload: PostPastedPayload): Promise<APIPastedResponse> {

		const url = `/pastes`

		const response = api_client.post<APIPastedResponse>(url, JSON.stringify(payload))

		return response

	}



	async function getPasted(shortcode: string): Promise<APIPastedResponse> {
		const url = `/pastes/?shortcode=${shortcode}`

		const response = api_client.get<APIPastedResponse>(url)

		return response
	}



  return { getToken, postPasted, getPasted, getApiCapabilities, getBranding }
}
