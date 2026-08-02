import { mount } from '@vue/test-utils'
import { describe, expect, test } from "vitest";
import PButton from "../PButton.vue";

describe("PButton component", () => {
	test("Respect the passed prop", () => {
		const wrapper = mount(PButton, {
			props: {
				text: "click me"
			}
		})
		expect(wrapper.text()).toContain("click me")
	})

	test("renders the icon slot", () => {
		const wrapper = mount(PButton, {
			props: {
				text: "Save"
			},
			slots: {
			  icon: "<svg data-test='icon'></svg>"
			}
		})

		expect(wrapper.find("[data-test='icon']").exists()).toBe(true)
	})
})
