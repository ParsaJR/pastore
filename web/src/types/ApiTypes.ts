export type APIPastedResponse = {
  // An object that has been returned in the response of successful post paste request.
  shortcode: string,
  content: string,
}

export type APIError = {
  statusText: string,
  detail: string,
}

export type APIToken = {
  access_token: string,
  token_type: string,
}


// Client API Contracts.

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
  privacy_policy: string,
}

export type PostPastedPayload = {
  content: string,
  expiry_code: string,
  is_one_time: boolean
}

// Administration API contracts

export type PasteSchema = {
  created_at: string, // ISODate. For example "2026-07-13T07:58:58.337578"
  content: string,    // The actual paste content
  view_count: number,
  is_one_time: boolean,
  shortcode: string,
  expires_at: string, // ISODate. For example "2026-07-13T07:58:58.337578"
  id: number,
  is_deleted: boolean,
  //   duration: string | null; // Discarding it because it's depricated.
};

export type APIAllPastesResponse = {
  items: PasteSchema[],
  total_items: number,
  current_page: number,
  page_size: number,
  total_pages: number,
}
