export type APIPastedResponse = {
  // An object that has been returned in the response of successful post paste request.
  shortcode: string,
  content: string,
}

export type APIError = {
  statusText: string,
  detail: string,
}


// API Contracts.

export type APICapabilities = {
  expiry_durations: {
    code: string,
    name: string,
  }[]
}

export type APIBranding = {
  app_name: string,
  support_email: string,
  app_description: string,
}

export type PostPastedPayload = {
  content: string,
  expiry_code: string,
  is_one_time: boolean
}
