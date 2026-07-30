import { createApiClient } from "@/apiClient/client"
import type { APIBranding, APICapabilities, APIPastedResponse, APIAllPastesResponse, APIToken, PostPastedPayload, APIError } from "@/types/ApiTypes"

type APICallback<T> = (...args: any[]) => Promise<T>

export async function handleWithToast<T>(callback: APICallback<T>, successCallback?: () => void): Promise<T|undefined> {
	try {
		const result =  await callback()
		successCallback?.()
		return result
	} catch (err) {
		const error = err as APIError

		useToast().add(
			{
				title: error.statusText,
				description: error.detail,
				color: "error",
			}
		)

		return undefined
	}
}

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

	async function putBranding(payload: APIBranding): Promise<void> {
		const token = localStorage.getItem("token")

		const url = `/management/branding`
		api_client.put(url, JSON.stringify(payload), { Authorization: `Bearer ${token}` })
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


	async function getAllPastes(page: number = 1, per_page: number = 10): Promise<APIAllPastesResponse> {
		const token = localStorage.getItem("token")
		const url = `/pastes/all?page=${page}&page_size=${per_page}`

		const response = api_client.get<APIAllPastesResponse>(url, { Authorization: `Bearer ${token}` })

		return response
	}



	return { getToken, postPasted, getPasted, getAllPastes, getApiCapabilities, getBranding, putBranding }
}
