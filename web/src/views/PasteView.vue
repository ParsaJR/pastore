<script setup lang="ts">
import { ref, watch, onMounted, computed } from 'vue'
import { codeToHtml } from 'shiki'

import { useAppStore } from '../stores/appStore'
import { useLanguageDetector, useShikiHighlighter } from '@/composables/language-detect'

const appState = useAppStore()


const highlighted = ref('')


const code = defineModel<string>('code')


watch(() => appState.isViewMode, async () => {
	if (appState.isViewMode && code.value) {
		const lang = useLanguageDetector(code.value)
		highlighted.value = useShikiHighlighter(code.value, lang)
	}
	// Execute the watcher's callback immediately once, on the first creation of the component.
}, { immediate: true })

</script>

<template>
	<div class="font-mono text-sm h-auto">
		<div v-if="appState.isViewMode" v-html="highlighted"
			class="h-full w-full resize-none outline-none overflow-auto"></div>

		<textarea v-else v-model="code" name="code" autocomplete="off" class="h-full w-full text-code-primary resize-none overflow-auto outline-none"
			:placeholder=appState.serviceMotd></textarea>
	</div>
</template>


<style scoped>
textarea::placeholder {
	opacity: 0.4
}
</style>
