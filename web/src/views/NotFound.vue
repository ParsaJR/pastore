<script setup lang="ts">
import { useRouter } from 'vue-router';

const router = useRouter()
setTimeout(() => {
    router.push("/")
}, 3000);

</script>
<template>

	<UError :error="{
		statusCode: 404,
		statusMessage: 'Page not found',
		message: `I'll get you to the home route. Sit tight.`,
	}" :clear="false" />
</template>
