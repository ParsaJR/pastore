import type { APIBranding, APICapabilities } from '@/types/ApiTypes'
import { marked } from 'marked'
import { defineStore } from 'pinia'

interface IAppState {
  serviceName: string,
  serviceDescription: string,
  serviceSupportEmail: string,
  privacy_policy: string,
  isViewMode: boolean,
  isSideBarVisible: boolean,
  apiCapabilities: APICapabilities,
}
export const useAppStore = defineStore('app', {
  state: (): IAppState => ({
    serviceName: "Javan's Pastebin",
    serviceDescription: "A generic pastebin service",
    serviceSupportEmail: "hi@example.com",
    privacy_policy: "",
    isViewMode: false,
    isSideBarVisible: false,
    apiCapabilities: {
      "expiry_durations": []
    },
  }),
  actions: {
    toggleSidebar() {
      this.isSideBarVisible = !this.isSideBarVisible
    },
    toggleViewMode() {
      this.isViewMode = !this.isViewMode
    },
    populateApiCapabilities(caps: APICapabilities) {
      this.apiCapabilities = caps;
    },
    async populateBranding(branding: APIBranding) {
      this.serviceName = branding.app_name
      this.serviceDescription = branding.app_description
      this.privacy_policy = await marked.parse(branding.privacy_policy)
    },
  }
})
