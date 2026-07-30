<script setup lang="ts">
import { handleWithToast, useAPI } from '@/composables/api';
import type { APIBranding, APIError } from '@/types/ApiTypes';
import type { FormSubmitEvent } from '@nuxt/ui';
import * as v from 'valibot'
import { ref } from 'vue';

const state = ref<APIBranding>({
	app_name: '',
	support_email: '',
	app_description: '',
	message_of_the_day: '',
	privacy_policy: '',
})

const branding = await handleWithToast(() => useAPI().getBranding())

if (branding) {
	state.value = branding
}

const schema = v.object({
	app_name: v.pipe(v.string(), v.nonEmpty()),
	support_email: v.pipe(v.string(), v.email()),
	app_description: v.string(),
	message_of_the_day: v.string(),
	privacy_policy: v.pipe(v.string(), v.nonEmpty())
})

type Schema = v.InferOutput<typeof schema>
async function onSubmit(event: FormSubmitEvent<Schema>) {
	handleWithToast(async () =>
		await useAPI().putBranding(state.value),
		() => {
			useToast().add({
				title: "Branding information has been successfully updated."
			})
		}
	)
}
</script>

<template>
	<UCard>
		<template #header>
			<h2 class="text-lg font-semibold">Branding</h2>
		</template>

		<UForm :state="state" :schema="schema" @submit="onSubmit" class="space-y-4">
			<UFormField name="app_name" label="App name">
				<UInput v-model="state.app_name" class="w-full" placeholder="Pastore" />
			</UFormField>

			<UFormField name="support_email" label="Support email">
				<UInput v-model="state.support_email" type="email" class="w-full" placeholder="support@example.com" />
			</UFormField>

			<UFormField name="app_description" label="Description">
				<UTextarea v-model="state.app_description" class="w-full" placeholder="Describe your application..." />
			</UFormField>

			<UFormField name="privacy_policy" label="Privacy policy" hint="Markdown aware">
				<UTextarea v-model="state.privacy_policy" class="w-full" placeholder="Enter your privacy policy..." />
			</UFormField>

			<UFormField name="message_of_the_day" label="Message of the day" hint="Optional">
				<UTextarea v-model="state.message_of_the_day" class="w-full"
					placeholder="A message shown to users..." />
			</UFormField>

			<div class="flex justify-end">
				<UButton type="submit">
					Save
				</UButton>
			</div>
		</UForm>
	</UCard>
</template>
