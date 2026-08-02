import { mount } from '@vue/test-utils'
import { describe, expect, test, vi } from "vitest"
import PHeader from '../PHeader.vue'
import { useAppStore } from '@/stores/appStore'

const toggleSidebarFunc = vi.fn()

vi.mock("@/stores/appStore", () => ({
	useAppStore: () => ({
		toggleSidebar: toggleSidebarFunc
	})
}))

describe("PHeader component", () => {
	test("The button actually toggles", async () => {
	  const wrapper = mount(PHeader)


	  await wrapper.find("button").trigger("click")

	  expect(toggleSidebarFunc).toHaveBeenCalledOnce()
	})
})
