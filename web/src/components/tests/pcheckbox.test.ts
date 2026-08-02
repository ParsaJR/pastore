import { mount } from '@vue/test-utils'
import { describe, expect, test } from "vitest"
import { ref } from 'vue'
import PCheckbox from '../PCheckbox.vue'


test("Respects the passed prop as a model", async () => {

const checked = ref(false)

const wrapper = mount(PCheckbox, {
  props: {
    modelValue: checked.value,
    "onUpdate:modelValue": (v) => checked.value = v
  }
})

await wrapper.find("input").setValue(true)

expect(checked.value).toBe(true)

})
