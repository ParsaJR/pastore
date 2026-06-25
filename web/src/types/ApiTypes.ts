export type ApiResponse = {
  shortCode: string,
  content: string,
}
export type ApiError = {
  statusText: string,
  detail: string,
}


// API Contracts.

export type ApiCapabilities = {
  expiry_durations: {
    code: string,
    name: string,
  }[]
}

export type APIBranding = {
  app_name: string,
  support_email: string,
  privacy_policy: string,
}

export type PostPastedPayload = {
  content: string,
  expiry_code: string,
  is_one_time: boolean
}
