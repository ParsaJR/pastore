import { createApiClient } from "@/apiClient/client"
import type { APIBranding, APICapabilities, APIPastedResponse, PostPastedPayload } from "@/types/ApiTypes"


export function useAPI() {
  const api_client = createApiClient({baseUrl: "/api"})

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

    const response = api_client.post<APIPastedResponse>(url,payload)

    return response

  }



  async function getPasted(shortcode: string): Promise<APIPastedResponse> {
    const url = `/pastes/?shortcode=${shortcode}`

    const response = api_client.get<APIPastedResponse>(url)

    return response
  }



  return { postPasted, getPasted, getApiCapabilities, getBranding }
}
