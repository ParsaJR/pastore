import type { APIBranding, APICapabilities } from '@/types/ApiTypes'
import { defineStore } from 'pinia'

interface IAppState {
  serviceName: string,
  serviceDescription: string,
  serviceSupportEmail: string,
  isViewMode: boolean,
  isSideBarVisible: boolean,
  apiCapabilities: APICapabilities
  modal: {
    isVisible: boolean,
    content: string,
  },
}
export const useAppStore = defineStore('app', {
  state: (): IAppState => ({
    serviceName: "Javan's Pastebin",
    serviceDescription: "A generic pastebin service",
    serviceSupportEmail: "hi@example.com",
    isViewMode: false,
    isSideBarVisible: false,
    apiCapabilities: {
      "expiry_durations": []
    },
    modal: {
      isVisible: false,
      content: "",
    }
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
    populateBranding(branding: APIBranding) {
      this.serviceName = branding.app_name
      this.serviceDescription = branding.app_description
    },
    toggleModal() {
      this.modal.isVisible = !this.modal.isVisible
    }
  }
})
